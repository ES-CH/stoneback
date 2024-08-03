from rest_framework import routers

from apps.inventory.views import (CompanyViewSet, InventoryViewSet,
                                  ProductViewSet)

router = routers.DefaultRouter(trailing_slash=False)


router.register(r'company', CompanyViewSet)
router.register(r'inventory', ProductViewSet)
router.register(r'', InventoryViewSet)
