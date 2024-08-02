from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.custom_auth.filters_backend import (ActiveRecordsFilter,
                                              UserRecordsFilter)
from apps.custom_auth.models import User
from apps.custom_auth.permissions import PermissionView, Roles
from apps.custom_auth.serializers import (MyTokenObtainPairSerializer,
                                          UserSerializer)

# Create your views here.


class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 401:
            username = request.data["username"]
            user = User.objects.filter(username=username).first()
            if user and not user.is_active:
                response.data["disabled"] = _("User account is disabled.")
                return super().finalize_response(request, response, *args, **kwargs)
        if response.data.get("refresh"):
            cookie_max_age = 3600 * 24  # 1 day
            response.set_cookie(
                "refresh_token",
                response.data["refresh"],
                samesite='None',
                secure=True,
                max_age=cookie_max_age,
                httponly=True,
            )

        # Get and process users permissions
        if response.data.get("access"):
            username = request.data["username"]
            user = User.objects.filter(username=username).first()
            current_permissions = list(
                user.get_all_permissions()) if user else []
            permissions = []
            for permission in current_permissions:
                if "historical" not in permission:
                    permissions.append(permission.split(".")[-1])
            response.data["permissions"] = permissions
        return super().finalize_response(request, response, *args, **kwargs)


class UserViewSet(PermissionView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [ActiveRecordsFilter, UserRecordsFilter]

    allowed_permissions = {
        "create": [Roles.ANY]
    }

    def create(self, request):
        email = request.data.get("email", None)
        if not email:
            return Response(
                {"email": ["This field is required."]},
                status.HTTP_400_BAD_REQUEST,
            )
        exist_user = User.objects.filter(email=email).first()
        if exist_user:
            return Response(
                {"email": ["This email is already in use."]},
                status.HTTP_400_BAD_REQUEST,
            )
        password = request.data.get("password")
        if not password:
            return Response(
                {"password": ["This field is required."]},
                status.HTTP_400_BAD_REQUEST,
            )
        request.data["password"] = make_password(password)
        process_email = str(email).strip().lower() if email else None
        request.data["username"] = process_email
        request.data["email"] = process_email
        serializer = UserSerializer(
            data=request.data, context={"request": request}, partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
