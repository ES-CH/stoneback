import jwt
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from apps.custom_auth.models import User


def change_active_status(instance):
    instance.is_active = False
    instance.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


def change_active_status_related(instance):
    related_objects = []
    models = apps.get_models()
    instance_model = instance.__class__
    for model in models:
        for field in model._meta.get_fields():
            if isinstance(field, ForeignKey) and field.related_model == instance_model:
                related_objects.extend(
                    model.objects.filter(**{field.name: instance.id}))
    for related_object in related_objects:
        change_active_status(related_object)


def update_refresh_token_date(token):
    decodeToken = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    user = User.objects.filter(id=decodeToken["user_id"]).first()
    user.last_refresh_token_date = timezone.now()
    user.save()


def validate_roles(roles):
    erros = []
    for role in roles:
        exist = Group.objects.filter(name=role).exists()
        if not exist:
            erros.append({role: "Role does not exist."})
    if erros:
        return erros
    return True


def validate_permissions(permissions):
    errors = []
    permissions_id = []

    for permission in permissions:
        model_errors = validate_model(permission)
        action_errors, valid_actions = validate_actions(permission)

        errors.extend(model_errors)
        errors.extend(action_errors)

        if not model_errors and not action_errors:
            permissions_id.extend(get_permission_ids(
                permission, valid_actions, errors))

    if errors:
        return errors
    return permissions_id


def validate_model(permission):
    errors = []
    if not permission.get("model"):
        errors.append({permission.get("model"): "Model is required."})
    return errors


def validate_actions(permission):
    errors = []
    valid_actions = []
    actions = permission.get("action")

    if not actions:
        errors.append({permission.get("model"): "Action is required."})
    elif len(actions) == 0:
        errors.append({permission.get("model"): "Action is required."})
    else:
        for action in actions:
            if action not in ["view", "add", "change", "delete"]:
                errors.append({"action": "Action is invalid."})
            else:
                valid_actions.append(action)
    return errors, valid_actions


def get_permission_ids(permission, valid_actions, errors):
    permissions_id = []
    for action in valid_actions:
        current_permission = Permission.objects.filter(
            codename=f"{action}_{permission.get('model')}"
        ).first()
        if not current_permission:
            errors.append(
                {f"{action}_{permission.get('model')}": "Permission does not exist."})
        else:
            permissions_id.append(current_permission.id)
    return permissions_id
