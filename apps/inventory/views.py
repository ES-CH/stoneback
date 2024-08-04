
from apps.custom_auth.filters_backend import ActiveRecordsFilter
from apps.custom_auth.permissions import (CustomDjangoModelPermissions,
                                          PermissionView)
from apps.inventory.models import Company, Inventory, Product
from apps.inventory.serializers import (CompanySerializer, InventorySerializer,
                                        ProductSerializer)


class CompanyViewSet(PermissionView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (CustomDjangoModelPermissions,)
    filter_backends = [ActiveRecordsFilter]


class ProductViewSet(PermissionView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (CustomDjangoModelPermissions,)
    filter_backends = [ActiveRecordsFilter]


class InventoryViewSet(PermissionView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = (CustomDjangoModelPermissions,)
    filter_backends = [ActiveRecordsFilter]
