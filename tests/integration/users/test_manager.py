from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import pytest

User = get_user_model()


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        username="testuser",
        first_name="Test",
        last_name="User",
        password="securepassword",
    )


@pytest.mark.integration
@pytest.mark.django_db
class TestCustomUserManager:

    def test_superuser_is_instance_of_user(self, superuser):
        assert isinstance(superuser, User)

    def test_create_superuser_with_valid_data(self, superuser):
        assert superuser.pk is not None
        assert superuser.username == "testuser"
        assert superuser.first_name == "Test"
        assert superuser.last_name == "User"
        assert superuser.check_password("securepassword")
        assert superuser.is_superuser is True
        assert superuser.is_staff is True

    def test_create_superuser_without_first_name_raises_error(self, superuser):
        superuser.first_name = ""
        with pytest.raises(ValidationError):
            superuser.full_clean()

    def test_create_superuser_without_username_raises_error(self, superuser):
        superuser.username = ""
        with pytest.raises(ValidationError):
            superuser.full_clean()

    def test_create_superuser_without_password_raises_error(self, superuser):
        superuser.password = ""
        with pytest.raises(ValidationError):
            superuser.full_clean()

    def test_create_superuser_without_last_name_does_not_raise_error(self, superuser):
        superuser.last_name = ""
        superuser.full_clean()
        assert superuser.last_name == ""

    def test_create_superuser_raises_integrity_error_when_duplicate_username(
        self, superuser
    ):
        with pytest.raises(IntegrityError):
            User.objects.create_superuser(
                username=superuser.username,
                first_name="Another",
                last_name="User",
                password="anotherpass",
            )

    def test_createsuperuser_method_with_short_password_raises_error(self):
        with pytest.raises(ValidationError):
            User.objects.create_superuser(
                username="shortpassuser",
                first_name="Short",
                last_name="Pass",
                password="123",
            )

    def test_create_superuser_method_password_is_hashed(self, superuser):
        assert superuser.password.startswith("pbkdf2_sha256$")
        assert superuser.password != "securepassword"
        assert superuser.check_password("securepassword")
