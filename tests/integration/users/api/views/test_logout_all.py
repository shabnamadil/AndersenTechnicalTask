import pytest
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
@pytest.mark.integration
class TestLogoutAllDevices:

    def test_successful_logout_blacklists_all_tokens(
        self, authenticated_client, user, logout_all_url
    ):
        # Create multiple tokens for the same user
        RefreshToken.for_user(user)
        RefreshToken.for_user(user)
        assert OutstandingToken.objects.filter(user=user).count() >= 2

        response = authenticated_client.post(logout_all_url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["detail"] == "All sessions have been logged out successfully."
        )

        # All tokens for user must now be blacklisted
        user_tokens = OutstandingToken.objects.filter(user=user)
        for token in user_tokens:
            assert BlacklistedToken.objects.filter(token=token).exists()

    def test_unauthenticated_request_fails(self, api_client, logout_all_url):
        response = api_client.post(logout_all_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_with_no_tokens_still_returns_success(
        self, authenticated_client, user, logout_all_url
    ):
        # Clear any tokens
        OutstandingToken.objects.filter(user=user).delete()

        response = authenticated_client.post(logout_all_url)
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["detail"] == "All sessions have been logged out successfully."
        )
