import datetime

import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
@pytest.mark.integration
class TestLogoutAPIView:

    def authenticate(self, client, tokens):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    def test_successful_logout_blacklists_token(self, api_client, logout_url, tokens):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = tokens["refresh"]
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_205_RESET_CONTENT

    def test_logout_fails_with_missing_refresh_token(
        self, api_client, logout_url, tokens
    ):
        self.authenticate(api_client, tokens)
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("token", ["invalid_token", "", None])
    def test_logout_fails_with_invalid_refresh_token(
        self, api_client, logout_url, tokens, token
    ):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = token
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_fails_with_expired_refresh_token(
        self, api_client, logout_url, tokens
    ):
        self.authenticate(api_client, tokens)
        expired = RefreshToken(tokens["refresh"])
        expired.set_exp(lifetime=datetime.timedelta(seconds=-1))
        api_client.cookies["refresh_token"] = str(expired)
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_fails_without_authentication(self, api_client, logout_url):
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_fails_with_invalid_access_token(
        self, api_client, logout_url, tokens
    ):
        api_client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        api_client.cookies["refresh_token"] = tokens["refresh"]
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_fails_with_blacklisted_refresh_token(
        self, api_client, logout_url, tokens
    ):
        refresh = RefreshToken(tokens["refresh"])
        refresh.blacklist()
        self.authenticate(api_client, {"access": tokens["access"]})
        api_client.cookies["refresh_token"] = str(refresh)
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_fails_with_blacklisted_access_token(
        self, api_client, logout_url, tokens
    ):
        refresh = RefreshToken(tokens["refresh"])
        refresh.blacklist()
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_fails_with_inactive_user(
        self, api_client, user, logout_url, tokens
    ):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = tokens["refresh"]
        user.is_active = False
        user.save()
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_double_logout(self, api_client, logout_url, tokens):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = tokens["refresh"]
        api_client.post(logout_url)  # First logout
        response = api_client.post(logout_url)  # Second logout
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_clears_refresh_cookie(self, api_client, logout_url, tokens):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = tokens["refresh"]
        response = api_client.post(logout_url)
        cookie = response.cookies.get("refresh_token")
        assert cookie is not None
        assert cookie.value == ""
        assert cookie["max-age"] == 0

    def test_logout_fails_with_tampered_refresh_token(
        self, api_client, logout_url, tokens
    ):
        self.authenticate(api_client, tokens)
        tampered = tokens["refresh"][:-1] + "misuse"
        api_client.cookies["refresh_token"] = tampered
        response = api_client.post(logout_url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
