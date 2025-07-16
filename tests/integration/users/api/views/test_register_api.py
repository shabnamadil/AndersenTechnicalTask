from django.contrib.auth import get_user_model

import pytest
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestRegisterAPI:

    def test_successful_registration(self, api_client, register_url, register_data):
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="jhon_doe").exists()

    @pytest.mark.parametrize(
        "field, value",
        [
            ("first_name", ""),
            ("username", ""),
            ("password", ""),
            ("password_confirm", ""),
        ],
    )
    def test_missing_fields(
        self, api_client, register_url, register_data, field, value
    ):
        register_data[field] = value
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field in response.data

    def test_password_mismatch(self, api_client, register_url, register_data):
        register_data["password_confirm"] = register_data["password"] + "_mismatch"
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password_confirm" in response.data

    def test_existing_username(self, api_client, register_url, register_data):
        User.objects.create_user(
            first_name="Jhon",
            last_name="Doe",
            username=register_data["username"],
            password="TestPass123!",
        )
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_weak_password(self, api_client, register_url, register_data):
        register_data["password"] = "weak"
        register_data["password_confirm"] = "weak"
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data
