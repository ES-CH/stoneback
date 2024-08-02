from email.headerregistry import Group

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)

from apps.custom_auth.models import User
from apps.custom_auth.utils import update_refresh_token_date


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):

        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            res = super().validate(attrs)
            update_refresh_token_date(res.get("access"))
            return res
        else:
            raise InvalidToken(
                "No valid token found in cookie 'refresh_token'")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        request_data = self.context['request'].data
        groups = []
        if 'groups' in request_data:
            groups = request_data.pop('groups')

        instance = User.objects.create(**validated_data)
        instance.set_password(validated_data['password'])
        if groups:
            instance.groups.set(groups)

        return instance
