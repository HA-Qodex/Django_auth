from rest_framework import serializers
from .models import *
from django.conf import settings


class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'email', 'username', 'phone', 'password', 'user_image')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id', 'username', 'email', 'phone', 'user_image']


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        # fields = '__all__'
        exclude = ['user_id', 'is_active']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = '__all__'
        depth = 1

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyModel
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'