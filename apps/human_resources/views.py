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
