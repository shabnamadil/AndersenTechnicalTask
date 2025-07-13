from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
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
    return reverse("logout_all")


@pytest.fixture
def authenticated_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


@pytest.mark.django_db
@pytest.mark.integration
class TestLogoutAllDevices:

    def test_successful_logout_blacklists_all_tokens(
        self, authenticated_client, user, url
    ):
        # Create multiple tokens for the same user
        RefreshToken.for_user(user)
        RefreshToken.for_user(user)
        assert OutstandingToken.objects.filter(user=user).count() >= 2

        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["detail"] == "All sessions have been logged out successfully."
        )

        # All tokens for user must now be blacklisted
        user_tokens = OutstandingToken.objects.filter(user=user)
        for token in user_tokens:
            assert BlacklistedToken.objects.filter(token=token).exists()

    def test_unauthenticated_request_fails(self, api_client, url):
        response = api_client.post(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_with_no_tokens_still_returns_success(
        self, authenticated_client, user, url
    ):
        # Clear any tokens
        OutstandingToken.objects.filter(user=user).delete()

        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["detail"] == "All sessions have been logged out successfully."
        )
