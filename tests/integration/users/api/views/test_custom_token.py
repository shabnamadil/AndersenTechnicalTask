from django.conf import settings
from django.utils import timezone

import pytest
from rest_framework import status

from tests.helpers.auth_helpers import decode_jwt


@pytest.mark.django_db
@pytest.mark.integration
class TestCustomTokenObtainPairView:

    def test_token_obtain_pair_returns_access_token_in_response(
        self, api_client, obtain_url, valid_credentials
    ):
        response = api_client.post(obtain_url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_token_obtain_pair_writes_refresh_token_in_cookie(
        self, api_client, obtain_url, valid_credentials
    ):
        response = api_client.post(obtain_url, valid_credentials, format="json")
        refresh_token_cookie = response.cookies.get("refresh_token")

        assert refresh_token_cookie is not None
        assert "httponly" in refresh_token_cookie
        # assert "secure" in refresh_token_cookie  # uncomment if using HTTPS
        assert refresh_token_cookie.get("samesite") == "Lax"

    def test_token_obtain_pair_with_invalid_credentials(
        self, api_client, obtain_url, invalid_credentials
    ):
        response = api_client.post(obtain_url, invalid_credentials, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_obtain_pair_with_missing_username(
        self, api_client, obtain_url, valid_credentials
    ):
        valid_credentials.pop("username")
        response = api_client.post(obtain_url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data

    def test_token_obtain_pair_with_missing_password(
        self, api_client, obtain_url, valid_credentials
    ):
        valid_credentials.pop("password")
        response = api_client.post(obtain_url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

    def test_token_obtain_pair_with_inactive_user(
        self, api_client, obtain_url, user, valid_credentials
    ):
        user.is_active = False
        user.save()
        response = api_client.post(obtain_url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_token_expiry(self, user, obtain_url, api_client, valid_credentials):

        # Step 1: Get token
        response = api_client.post(obtain_url, valid_credentials, format="json")
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
