from django.apps import apps
from django.db.models.fields.related import ForeignKey
from rest_framework import status
from rest_framework.response import Response


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
