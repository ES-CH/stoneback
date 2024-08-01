from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.custom_auth.models import User


# Custom classes
class AbstractUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'identification_number',
                    'phone_number'
                ),
            },
        ),
    )


# Register your models here.
admin.site.register(User, AbstractUserAdmin)
