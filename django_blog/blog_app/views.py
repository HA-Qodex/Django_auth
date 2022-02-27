from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class Registration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
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
            # return Response(response_message)
        except Exception as e:
            response_message = {
                "success": False,
                "message": str(e),
                "data": "",
                "error": "",
                "error_code": 400
            }
        return Response(response_message)
