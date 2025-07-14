import datetime

import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
@pytest.mark.integration
class TestCustomTokenRefreshView:

    def test_refresh_token_not_found_in_cookie_without_login(
        self, api_client, refresh_url, valid_credentials
    ):
        response = api_client.post(refresh_url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not response.cookies.get("refresh_token")
        assert response.data == {"detail": "Refresh token not found in cookie"}

    def test_refresh_token_found_in_cookie_after_login(
        self, api_client, obtain_url, valid_credentials
    ):
        response = api_client.post(obtain_url, valid_credentials, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.cookies.get("refresh_token")

    def test_refresh_token_view_returns_new_access_token(
        self, api_client, obtain_url, refresh_url, valid_credentials
    ):
        response = api_client.post(obtain_url, valid_credentials, format="json")
        refresh_token_cookie = response.cookies.get("refresh_token")

        refresh_response = api_client.post(
            refresh_url, {"refresh": refresh_token_cookie.value}, format="json"
        )

        assert refresh_response.status_code == status.HTTP_200_OK
        assert "access" in refresh_response.data

    def test_expired_refresh_token_returns_401(self, api_client, refresh_url, user):
        refresh_token = RefreshToken.for_user(user)
        refresh_token.set_exp(lifetime=datetime.timedelta(seconds=-1))
        api_client.cookies["refresh_token"] = str(refresh_token)
        response = api_client.post(refresh_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Invalid or expired refresh token"
