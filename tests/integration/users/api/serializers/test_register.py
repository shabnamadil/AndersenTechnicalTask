from django.contrib.auth import get_user_model

import pytest

from apps.users.api.serializers import RegisterSerializer

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestRegisterSerializer:

    @pytest.mark.parametrize(
        "field, value",
        [
            ("first_name", ""),
            ("username", ""),
            ("password", ""),
            ("password_confirm", ""),
        ],
    )
    def test_missing_required_fields(self, field, value, register_data):
        register_data[field] = value
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert field in serializer.errors

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
            username="jhon_doe",
            first_name="Existing",
            last_name="User",
            password="AnotherPass123!",
        )
        serializer = RegisterSerializer(data=register_data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors

    def test_valid_registration(self, register_data):
        serializer = RegisterSerializer(data=register_data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.username == register_data["username"]
        assert user.first_name == register_data["first_name"]
        assert user.check_password(register_data["password"])
        assert user.last_name == register_data.get("last_name", "")
