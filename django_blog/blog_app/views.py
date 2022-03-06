from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
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
                    "errors": serializer.errors,
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

    # ------------------------- POST -------------------------

    queryset = PostModel.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user)

    # -------------------------- POST with Serializer ------------------

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

    # ---------------------------- GET with Serializer --------------------

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_success_headers(page, many=True)
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

#------------------------------------ Filter ---------------------------

    # def get_queryset(self):
    #     return BlogPostModel.objects.filter(is_active=False)


class PostUpdate(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = PostModel.objects.filter(is_active=True)
    serializer_class = BlogSerializer
    lookup_field = 'id'

#----------------------------- RETRIVE with Serializer --------------------

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostSerializer(instance)
        response_message = {
            "success": True,
            "message": "",
            "data": serializer.data,
            "error": "",
            "error_code": 200
        }
        return Response(response_message)

#----------------------------- UPDATE with Serializer --------------------

    def perform_update(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance=self.perform_update(serializer)
        serializer = PostSerializer(instance, many=False)

        response_message = {
            "success": True,
            "message": "",
            "data": serializer.data,
            "error": "",
            "error_code": 200
        }

        return Response(response_message)

#---------------------------- Temporary Delete ----------------------------------

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

#-----------------------------Permanent DELETE with Serializer --------------------

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_message = {
            "success": True,
            "message": "Post has been deleted",
            "data": "",
            "error": "",
            "error_code": 200
        }
        return Response(response_message, status=status.HTTP_204_NO_CONTENT)
