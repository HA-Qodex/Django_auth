from django.contrib import admin
from .models import *

admin.site.register([NewUser, PostModel, CommentModel, ReplyModel, LikeModel, CategoryModel])
