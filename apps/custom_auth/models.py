from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def user_can_retrieve_me(self, obj, user):
        return obj.id == user.id or user.groups.filter(name='admin').exists() or user.is_superuser
