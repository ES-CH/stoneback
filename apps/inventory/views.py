
from apps.custom_auth.filters_backend import ActiveRecordsFilter
from apps.custom_auth.permissions import (CustomDjangoModelPermissions,
                                          PermissionView)
from apps.inventory.models import Inventory
from apps.inventory.serializers import InventorySerializer

# Create your views here.


class InventoryViewSet(PermissionView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = (CustomDjangoModelPermissions,)
    filter_backends = [ActiveRecordsFilter]
    allowed_permissions = {
        'inventory_bulk_upload': ["inventory.add_inventory"],
        'inventory_report': ["inventory.view_inventory"],
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return InventorySerializer
        return InventorySerializer
