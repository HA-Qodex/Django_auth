from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *


class Registration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                # refresh_token = RefreshToken.for_user(serializer)
                response_message = {
                    "success": True,
                    "message": "User has been registered",
                    # "token": refresh_token,
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


# class LoginView(TokenObtainPairView):
#     serializer = TokenSerializer

def loginView(APIView):
    def post(self, request):
        user = NewUser.objects.get(email=request.data['email'])
        print(user)
        return Response()
