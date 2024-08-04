
from apps.accounting.models import Accounting
from apps.accounting.serializers import AccountingSerializer
from apps.custom_auth.filters_backend import ActiveRecordsFilter
from apps.custom_auth.permissions import (CustomDjangoModelPermissions,
                                          PermissionView)


class AccountViewSet(PermissionView):
    queryset = Accounting.objects.all()
    serializer_class = AccountingSerializer
    permission_classes = (CustomDjangoModelPermissions,)
    filter_backends = [ActiveRecordsFilter]
