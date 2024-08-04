from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.custom_auth.models import User


class AbstractUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
    )


# Register your models here.
admin.site.register(User, AbstractUserAdmin)
