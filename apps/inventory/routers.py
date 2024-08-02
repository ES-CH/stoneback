from rest_framework import routers

from apps.inventory.views import InventoryViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'', InventoryViewSet)
