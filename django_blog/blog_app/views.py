from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.conf import settings


class Registration(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NewUserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                response_message = {
                    "success": True,
                    "message": "User has been registered",
                    "data": "",
                    "error": "",
                    "error_code": 200
                }
            else:
                response_message = {
                    "success": False,
                    "message": "User registration failed",
                    "data": "",
                    "error": serializer.errors[next(iter(serializer.errors))][0],
                    "error_code": 401
                }
        except Exception as e:
            response_message = {
                "success": False,
                "message": str(e),
                "data": "",
                "error": "",
                "error_code": 400
            }
        return Response(response_message)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = NewUser.objects.get(email=request.data['email'])
        print(user)
        if user is not None:
            refresh_token = RefreshToken.for_user(user)
            response_message = {
                "success": True,
                "message": "Login Successful",
                "access_token": str(refresh_token.access_token),
                "refresh": str(refresh_token),
                "lifetime": str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days)+" days",
                "data": "",
                "error": "",
                "error_code": 200
            }
        else:
            response_message = {
                "success": False,
                "message": "Login failed",
                "access_token": "",
                "refresh": "",
                "lifetime": "",
                "data": "",
                "error": "",
                "error_code": 401
            }
        return Response(response_message)


class ViewCheck(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response("This is check view")
