from django.urls import include, re_path

from apps.accounting.routers import router

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
