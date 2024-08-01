from rest_framework import routers

from apps.company.views import CompaniesViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'', CompaniesViewSet)
