from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import pytest

from tests.factories import UserFactory

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestUserCreation:

    def test_create_user_with_valid_data(self, user):
        assert user.pk is not None
        assert user.username.startswith("user")
        assert user.first_name != ""
        assert user.last_name != ""

    @pytest.mark.parametrize(
        "field, value",
        [
            ("first_name", ""),
            ("username", ""),
            ("password", ""),
        ],
    )
    def test_required_fields_raise_validation_error(self, user, field, value):
        setattr(user, field, value)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_without_last_name_does_not_raise_error(self, user):
        user.last_name = ""
        user.full_clean()
        assert user.last_name == ""

    def test_username_uniqueness(self, user):
        with pytest.raises(IntegrityError):
            UserFactory(username=user.username)

    def test_create_user_with_short_password(self):
        with pytest.raises(ValidationError):
            User.objects.create_user(username="u1", password="123")

    def test_password_is_hashed(self, user):
        assert user.password.startswith("pbkdf2_sha256$")
        assert user.password != "securepassword"
        assert user.check_password("securepassword")

    def test_create_user_does_not_create_superuser(self, user):
        assert not user.is_superuser
        assert not user.is_staff

    def test_user_is_instance_of_custom_user(self, user):
        assert isinstance(user, User)
