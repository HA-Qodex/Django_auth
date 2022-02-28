from django.urls import path
from .views import *
from .serializers import *

urlpatterns = [
    path('registration/', Registration.as_view(), name="create_user"),
    path('login/', LoginView.as_view(), name="user_login"),
]
