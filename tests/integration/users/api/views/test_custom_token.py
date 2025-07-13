from django.conf import settings
from django.urls import reverse
from django.utils import timezone

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.utils.factories import UserFactory
from tests.utils.helpers import decode_jwt


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def url():
    return reverse("custom_token_obtain_pair")


@pytest.fixture
def valid_credentials(user):
    return {"username": user.username, "password": "securepassword"}


@pytest.fixture
def invalid_credentials():
    return {"username": "wronguser", "password": "wrongpass"}


@pytest.mark.django_db
@pytest.mark.integration
class TestCustomTokenObtainPairView:

    def test_token_obtain_pair_returns_access_token_in_response(
        self, api_client, url, valid_credentials
    ):
        response = api_client.post(url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_token_obtain_pair_writes_refresh_token_in_cookie(
        self, api_client, url, valid_credentials
    ):
        response = api_client.post(url, valid_credentials, format="json")
        refresh_token_cookie = response.cookies.get("refresh_token")

        assert refresh_token_cookie is not None
        assert "httponly" in refresh_token_cookie
        # assert "secure" in refresh_token_cookie  # uncomment if using HTTPS
        assert refresh_token_cookie.get("samesite") == "Lax"

    def test_token_obtain_pair_with_invalid_credentials(
        self, api_client, url, invalid_credentials
    ):
        response = api_client.post(url, invalid_credentials, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_obtain_pair_with_missing_username(
        self, api_client, url, valid_credentials
    ):
        valid_credentials.pop("username")
        response = api_client.post(url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_token_obtain_pair_with_missing_password(
        self, api_client, url, valid_credentials
    ):
        valid_credentials.pop("password")
        response = api_client.post(url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

    def test_token_obtain_pair_with_inactive_user(
        self, api_client, url, user, valid_credentials
    ):
        user.is_active = False
        user.save()
        response = api_client.post(url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_token_expiry(self, user, url, api_client, valid_credentials):

        # Step 1: Get token
        response = api_client.post(url, valid_credentials, format="json")
        assert response.status_code == 200
        access_token = response.data.get("access")
        assert access_token is not None

        # Step 2: Decode the JWT
        decoded_token = decode_jwt(access_token)
        exp_timestamp = decoded_token["exp"]
        expected_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]

        # Step 3: Compare with now + ACCESS_TOKEN_LIFETIME
        expected_exp = (timezone.now() + expected_lifetime).timestamp()
        assert abs(expected_exp - exp_timestamp) < 10  # 10 seconds buffer
