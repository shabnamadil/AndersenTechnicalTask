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
def authenticated_client(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.mark.integration
@pytest.mark.django_db
class TestAPIUrls:

    def test_register_api_get_not_allowed(self, api_client):
        url = reverse("register")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_custom_token_obtain_pair_api_get_not_allowed(self, api_client):
        url = reverse("custom_token_obtain_pair")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_token_refresh_api_get_not_allowed(self, api_client):
        url = reverse("custom_token_refresh")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_logout_api_get_not_allowed(self, authenticated_client):
        url = reverse("logout")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_logout_all_devices_api_get_not_allowed(self, authenticated_client):
        url = reverse("logout_all")
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
