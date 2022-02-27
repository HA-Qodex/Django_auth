from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, phone, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff = True.')
        if other_fields.get('is_admin') is not True:
            raise ValueError('Superuser must be assigned to is_admin = True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser = True.')

        return self.create_user(email, username, phone, password, **other_fields)

    def create_user(self, email, username, phone, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    phone = models.CharField(max_length=11, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.email
