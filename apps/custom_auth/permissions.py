import copy

from rest_framework import permissions, viewsets
from rest_framework.permissions import DjangoModelPermissions

from apps.custom_auth.utils import (change_active_status,
                                    change_active_status_related)


class Roles:
    ANY = '*',
    ADMIN = 'admin',


class PermissionView(viewsets.ModelViewSet):
    """
    Base class for permissions.

    use the `allowed_roles` property to define the allowed roles for each action.

    Example:

    class MyView(PermissionView):
        allowed_permissions = {
            'list': "custom_auth.view_user",
            'create': "custom_auth.add_user",
            'retrieve':["custom_auth.view_user", "custom_auth.view_profile"],
            ...
        }
    """

    def get_permissions(self):
        try:
            return [UserPermission(self.allowed_permissions[self.action])]
        except Exception:
            return [permission() for permission in self.permission_classes]

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, 'is_active'):
            response = change_active_status(instance)
            if response.status_code == 204:
                change_active_status_related(instance)
            return response
        else:
            return super().destroy(request, *args, **kwargs)


class UserPermission(permissions.BasePermission):
    def __init__(self, permissions):
        if type(permissions) is not list:
            permissions = [permissions]
        self.permissions = permissions

    def has_permission(self, request, view):
        user = request.user
        for permission in self.permissions:
            if permission == Roles.ANY or user.has_perm(permission):
                return True
        return False


class RolePermission(permissions.BasePermission):
    def __init__(self, roles):
        if type(roles) is not list:
            roles = [roles]
        self.roles = roles

    def has_permission(self, request, view):
        for role in self.roles:
            if role == Roles.ANY or request.user.groups.filter(name=role).exists():
                return True
        return False


class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
