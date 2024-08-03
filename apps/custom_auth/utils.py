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
    erros = []
    permissions_id = []
    for permission in permissions:
        if not permission.get("model"):
            erros.append({permission: "Model is required."})
        if len(permission.get("action")) == 0:
            erros.append({permission: "Action is required."})
        for action in permission.get("action"):
            if action not in ["view", "add", "change", "delete"]:
                erros.append({action: "Action is invalid."})
            current_permission = Permission.objects.filter(
                codename=f"{action}_{permission.get('model')}"
            ).first()
            if not current_permission:
                erros.append(
                    {f"{action}_{permission.get('model')}": "Permission does not exist."})
            else:
                permissions_id.append(current_permission.id)
    if erros:
        return erros
    return permissions_id
