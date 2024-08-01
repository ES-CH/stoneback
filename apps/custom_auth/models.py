from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from simple_history import register


class User(AbstractUser):
    identification_number = models.CharField(
        max_length=10, validators=[MinLengthValidator(6)], unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)

    def user_can_retrieve_me(self, obj, user):
        return obj.id == user.id or user.groups.filter(name='admin').exists() or user.is_superuser


register(User)
