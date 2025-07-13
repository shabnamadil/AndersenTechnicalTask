from django.contrib.auth import get_user_model

import pytest

from apps.users.api.serializers import RegisterSerializer

User = get_user_model()


@pytest.fixture
def register_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "username": "john_doe",
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
    }


@pytest.mark.integration
@pytest.mark.django_db
class TestRegisterSerializer:

    def test_missing_first_name(self, register_data):
        register_data["first_name"] = None
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors

    def test_missing_username(self, register_data):
        register_data["username"] = None
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors

    def test_missing_password(self, register_data):
        register_data["password"] = None
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_missing_password_confirm(self, register_data):
        register_data["password_confirm"] = register_data["password"] + "_mismatch"
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert "password_confirm" in serializer.errors

    def test_passwords_do_not_match(self, register_data):
        register_data["password_confirm"] = register_data["password"] + "_mismatch"
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert "password_confirm" in serializer.errors

    def test_weak_password(self, register_data):
        weak_password = "1234"
        register_data["password"] = weak_password
        register_data["password_confirm"] = weak_password
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_username_already_registered(self, register_data):
        User.objects.create_user(
            username="john_doe",
            first_name="Existing",
            last_name="User",
            password="AnotherPass123!",
        )
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors
