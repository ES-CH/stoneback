from rest_framework_simplejwt.views import TokenObtainPairView

from apps.custom_auth.serializers import MyTokenObtainPairSerializer

# Create your views here.


class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
