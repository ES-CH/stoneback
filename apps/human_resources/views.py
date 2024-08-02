from apps.custom_auth.filters_backend import ActiveRecordsFilter
from apps.custom_auth.permissions import (CustomDjangoModelPermissions,
                                          PermissionView)
from apps.human_resources.models import Employee
from apps.human_resources.serializers import EmployeeSerializer


class EmployeeViewSet(PermissionView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (CustomDjangoModelPermissions,)
    filter_backends = [ActiveRecordsFilter]
    allowed_permissions = {
        'employee_bulk_upload': ["human_resources.add_employee"],
        'employee_report': ["human_resources.view_employee"],
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeSerializer
        return EmployeeSerializer
