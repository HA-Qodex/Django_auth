from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', Registration.as_view(), name="create_user"),
    path('login/', LoginView.as_view(), name="user_login"),
    path('posts/', PostView.as_view(), name="post"),
    path('post_update/<int:id>/', PostUpdate.as_view(), name="post_update"),
    path('category/', CategoryView.as_view(), name="category"),
    path('category/<int:id>/', DeleteCategoryView.as_view(), name="category_delete"),
    path('comment/', CommentView.as_view(), name="comment"),
]