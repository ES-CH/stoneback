from rest_framework import routers

from apps.accounting.views import AccountViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'', AccountViewSet)
