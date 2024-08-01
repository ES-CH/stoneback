from apps.company.models import Company
from apps.company.serializers import CompanySerializer
from apps.custom_auth.permissions import CustomDjangoModelPermissions, PermissionView

# Create your views here.


class CompaniesViewSet(PermissionView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (CustomDjangoModelPermissions,)
    allowed_permissions = {
        'company_bulk_upload': ["company.add_company"],
        'company_report': ["company.view_company"],
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanySerializer
        return CompanySerializer
