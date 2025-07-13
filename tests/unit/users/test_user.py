from django.contrib.auth import get_user_model

import pytest

from apps.users.manager.custom_user_manager import CustomUserManager

User = get_user_model()


@pytest.mark.unit
class TestUserModel:
    def test_first_name_field_max_length(self):
        field = User._meta.get_field("first_name")
        assert field.max_length == 30

    def test_username_field_max_length(self):
        field = User._meta.get_field("username")
        assert field.max_length == 150

    def test_verbose_name_meta(self):
        assert User._meta.verbose_name == "User"
        assert User._meta.verbose_name_plural == "Users"

    def test_required_fields(self):
        assert User.REQUIRED_FIELDS == ["first_name", "last_name"]

    def test_custom_manager_type(self):
        assert isinstance(User.objects, CustomUserManager)

    def test_full_name_returns_get_full_name(self, mocker):
        user = User(username="johndoe", first_name="John", last_name="Doe")
        mocker.patch.object(user, "get_full_name", return_value="John Doe")
        assert user.full_name == "John Doe"

    def test_full_name_fallback_to_default(self, mocker):
        user = User(username="adminuser")
        mocker.patch.object(user, "get_full_name", return_value="")
        assert user.full_name == "Admin User"

    def test_str_method_returns_full_name(self, mocker):
        user = User(username="johndoe")
        mocker.patch.object(user, "get_full_name", return_value="Test User")
        assert str(user) == "Test User"
