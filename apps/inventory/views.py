
from apps.custom_auth.filters_backend import ActiveRecordsFilter
from apps.custom_auth.permissions import (CustomDjangoModelPermissions,
                                          PermissionView)
from apps.inventory.models import Company, Inventory
from apps.inventory.serializers import CompanySerializer, InventorySerializer

# Create your views here.


class CompanyViewSet(PermissionView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (CustomDjangoModelPermissions,)
    filter_backends = [ActiveRecordsFilter]

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanySerializer
        return CompanySerializer


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
