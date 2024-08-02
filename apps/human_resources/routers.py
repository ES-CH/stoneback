from rest_framework import routers

from apps.human_resources.views import EmployeeViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'', EmployeeViewSet)
