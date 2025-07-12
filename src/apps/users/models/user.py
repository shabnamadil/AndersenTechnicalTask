from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from apps.users.manager.custom_user_manager import CustomUserManager


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)

    email: str = ""
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects: ClassVar[CustomUserManager] = CustomUserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def full_name(self):
        return self.get_full_name() or "Admin User"

    def __str__(self):
        return self.full_name

    def clean(self):
        if len(self.password) < 6:
            raise ValidationError(
                {"password1": "Password must be at least 6 characters long."}
            )
        return self.password
