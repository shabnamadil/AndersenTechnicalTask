from typing import TYPE_CHECKING, Generic, TypeVar

from django.contrib.auth.models import UserManager
from django.contrib.auth.password_validation import validate_password

if TYPE_CHECKING:
    from apps.users.models import CustomUser

T = TypeVar("T", bound="CustomUser")


class CustomUserManager(UserManager[T], Generic[T]):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set.")
        if password:
            validate_password(password)
        if not extra_fields.get("first_name"):
            raise ValueError("The first name field must be set.")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)
