from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):

        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token
