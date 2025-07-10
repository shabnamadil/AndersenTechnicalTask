from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from apps.users.manager.custom_user_manager import CustomUserManager


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)

    email = None
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("-username",)
        indexes = [models.Index(fields=["username"])]

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    @property
    def full_name(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return "Admin User"

    def __str__(self):
        return self.full_name
    
    def clean(self):
        if len(self.password) < 6:
            raise ValidationError({"password1": "Password must be at least 6 characters long."})
        return self.password