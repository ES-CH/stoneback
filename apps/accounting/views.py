
from apps.accounting.models import Accounting
from apps.accounting.serializers import AccountingSerializer
from apps.custom_auth.filters_backend import ActiveRecordsFilter
from apps.custom_auth.permissions import (CustomDjangoModelPermissions,
                                          PermissionView)


# Create your views here.
class AccountViewSet(PermissionView):
    queryset = Accounting.objects.all()
    serializer_class = AccountingSerializer
    permission_classes = (CustomDjangoModelPermissions,)
    filter_backends = [ActiveRecordsFilter]
    allowed_permissions = {
        'account_bulk_upload': ["accounting.add_accounting"],
        'account_report': ["accounting.view_accounting"],
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountingSerializer
        return AccountingSerializer
