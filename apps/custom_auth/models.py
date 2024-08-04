from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def user_can_retrieve_me(self, obj, user):
        return obj.id == user.id or user.groups.filter(name='admin').exists() or user.is_superuser


class CommonModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
