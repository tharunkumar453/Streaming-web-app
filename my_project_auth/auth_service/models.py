from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUserModel(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        
        blank=False
    )

    phone = models.CharField(
        max_length=10,
        unique=True,
         
    )

    avatar_url = models.URLField(
        max_length=2000,
        null=True,
        blank=True,
        default=None
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = CustomUserManager()

    def __str__(self):
        return f"EMAIL: {self.email} && PHONE: {self.phone}"