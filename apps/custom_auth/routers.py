from rest_framework import routers

from apps.custom_auth.views import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet)
