from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('email', 'username', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['type'] = "Bearer"
        data['username'] = str(self.user)
        data['lifetime'] = str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days)+" day"
        print(str(self.user))
        return data

# class LoginView(TokenObtainPairView):
#     serializer = TokenSerializer