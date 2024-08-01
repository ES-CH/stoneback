import json
import os

import yaml
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db import transaction

FILE_CONTENT_LOADER = {"json": json.load, "yaml": yaml.safe_load, "yml": yaml.safe_load}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('permission_file', nargs='?', type=str)

    @transaction.atomic()
    def handle(self, *args, **options):
        permission_file = options["permission_file"]
        file = permission_file if permission_file else os.path.join(
            settings.BASE_DIR, 'apps/custom_auth/fixtures/initial_groups.yaml')
        groups = self.load_and_validate_file(file)

        group_count_loaded = 0
        for group in groups:
            group_count_loaded = self.create_groups_with_permissions(group, group_count_loaded)

        if group_count_loaded > 0:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully loaded {group_count_loaded} of {len(groups)} group(s)'))

    def create_groups_with_permissions(self, group, group_count_loaded):
        """Create the group and attach the provided permissions to it.

        Steps:
          - Get or create group object;
          - Add permissions (if defined) to group.

        """
        name = group['name']
        group_obj, _ = Group.objects.get_or_create(name=name)
        if 'permissions' in group:
            permissions = group['permissions']
            permissions_id = []
            for codename in permissions:
                permission = Permission.objects.filter(codename=codename).first()
                if permission:
                    permissions_id.append(permission.id)
                else:
                    self.stdout.write(
                        self.style.WARNING(f"No permissions codename defined for {codename}")
                    )
            if permissions_id or len(permissions) == 0:
                group_obj.permissions.set(permissions_id)
                group_count_loaded += 1
        return group_count_loaded

    def load_and_validate_file(self, permissions_file):
        """Load and validate the file contents.

        Steps:
          - Check if there is a valid loader for the provided file (by
            extension);
          - Load the contents of the file with the appropiate loader;

        """
        filename, ext = os.path.splitext(permissions_file)

        if ext[1:] not in FILE_CONTENT_LOADER.keys():
            self.stdout.write(self.style.ERROR(f"No loader found for extension: {ext}"))
            return None

        loader = FILE_CONTENT_LOADER[ext[1:]]
        with open(permissions_file, "r") as stream:
            file_content = loader(stream)

        return file_content
