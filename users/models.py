from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .managers import CustomUserManager


# class CustomUser(AbstractUser):
#     email = models.EmailField(_('Email'), unique=True)
#     username = models.CharField(max_length=150, unique=True, blank=True)
#     name = models.CharField(null=True,blank=True, max_length=255)
#     address = models.TextField(null=True, blank=True)
#     phone = models.BigIntegerField(null=True, blank=True)

#     # def get_absolute_url(self):
#     #     return reverse("users:detail", kwargs={"username": self.username})

#     def __str__(self):
#         return self.username

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    address = models.TextField(null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True
