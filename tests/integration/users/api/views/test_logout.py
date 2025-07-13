import datetime

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tests.utils.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def url():
    return reverse("logout")


@pytest.fixture
def tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@pytest.mark.django_db
@pytest.mark.integration
class TestLogoutAPIView:

    def authenticate(self, client, tokens):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    def test_successful_logout_blacklists_token(self, api_client, url, tokens):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = tokens["refresh"]
        response = api_client.post(url)
        assert response.status_code == status.HTTP_205_RESET_CONTENT

    def test_logout_fails_with_missing_refresh_token(self, api_client, url, tokens):
        self.authenticate(api_client, tokens)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize("token", ["invalid_token", "", None])
    def test_logout_fails_with_invalid_refresh_token(
        self, api_client, url, tokens, token
    ):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = token
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_fails_with_expired_refresh_token(self, api_client, url, tokens):
        self.authenticate(api_client, tokens)
        expired = RefreshToken(tokens["refresh"])
        expired.set_exp(lifetime=datetime.timedelta(seconds=-1))
        api_client.cookies["refresh_token"] = str(expired)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_fails_without_authentication(self, api_client, url):
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_fails_with_invalid_access_token(self, api_client, url, tokens):
        api_client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        api_client.cookies["refresh_token"] = tokens["refresh"]
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_fails_with_blacklisted_refresh_token(self, api_client, url, tokens):
        refresh = RefreshToken(tokens["refresh"])
        refresh.blacklist()
        self.authenticate(api_client, {"access": tokens["access"]})
        api_client.cookies["refresh_token"] = str(refresh)
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_fails_with_blacklisted_access_token(self, api_client, url, tokens):
        refresh = RefreshToken(tokens["refresh"])
        refresh.blacklist()
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_fails_with_inactive_user(self, api_client, user, url, tokens):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = tokens["refresh"]
        user.is_active = False
        user.save()
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_double_logout(self, api_client, url, tokens):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = tokens["refresh"]
        api_client.post(url)  # First logout
        response = api_client.post(url)  # Second logout
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_clears_refresh_cookie(self, api_client, url, tokens):
        self.authenticate(api_client, tokens)
        api_client.cookies["refresh_token"] = tokens["refresh"]
        response = api_client.post(url)
        cookie = response.cookies.get("refresh_token")
        assert cookie is not None
        assert cookie.value == ""
        assert cookie["max-age"] == 0

    def test_logout_fails_with_tampered_refresh_token(self, api_client, url, tokens):
        self.authenticate(api_client, tokens)
        tampered = tokens["refresh"][:-1] + "misuse"
        api_client.cookies["refresh_token"] = tampered
        response = api_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
