from django.urls import include, path, re_path

from apps.custom_auth.routers import router
from apps.custom_auth.views import CookieTokenObtainPairView

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('token/', CookieTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
