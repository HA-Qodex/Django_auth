from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
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
        serializer = UserSerializer(user, many=False)
        try:
            if user is not None:
                refresh_token = RefreshToken.for_user(user)
                response_message = {
                    "success": True,
                    "message": "Login Successful",
                    "access_token": "Bearer "+str(refresh_token.access_token),
                    "refresh": "Bearer "+str(refresh_token),
                    "lifetime": str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days)+" days",
                    "data": {"userdata": serializer.data},
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
        except Exception as e:
            response_message = {
                "success": False,
                "message": "Login failed",
                "access_token": "",
                "refresh": "",
                "lifetime": "",
                "data": "",
                "error": str(e),
                "error_code": 401
            }
        return Response(response_message)


class PostView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = BlogPostModel.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        serializer = PostSerializer(instance, many=False)

        response_message = {
            "success": True,
            "message": "Data has been saved successfully",
            "data": serializer.data,
            "error": "",
            "error_code": 200
        }

        return Response(response_message, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)

        response_message = {
            "success": True,
            "message": "",
            "data": serializer.data,
            "error": "",
            "error_code": 200
        }

        return Response(response_message)

    def get_queryset(self):
        queryset = BlogPostModel.objects.filter(is_active=True)
        return queryset
