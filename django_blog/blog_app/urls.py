from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', Registration.as_view(), name="create_user"),
]
