# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    pin = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)  # OTP later
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone"
