from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def register_url():
    return reverse("register")


@pytest.fixture
def register_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "username": "jhon_doe",
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
    }


@pytest.mark.django_db
@pytest.mark.integration
class TestRegisterAPI:

    def test_successful_registration(self, api_client, register_url, register_data):
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username="jhon_doe").exists()

    def test_missing_first_name(self, api_client, register_url, register_data):
        register_data.pop("first_name")
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "first_name" in response.data

    def test_missing_username(self, api_client, register_url, register_data):
        register_data.pop("username")
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_missing_password(self, api_client, register_url, register_data):
        register_data.pop("password")
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

    def test_missing_password_confirm(self, api_client, register_url, register_data):
        register_data.pop("password_confirm")
        response = api_client.post(register_url, register_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password_confirm" in response.data

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
