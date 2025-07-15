import pytest
from rest_framework import status


@pytest.mark.integration
@pytest.mark.django_db
class TestUsersAPIUrls:

    def test_register_api_get_not_allowed(self, api_client, register_url):
        response = api_client.get(register_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_custom_token_obtain_pair_api_get_not_allowed(self, api_client, obtain_url):
        response = api_client.get(obtain_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_token_refresh_api_get_not_allowed(self, api_client, refresh_url):
        response = api_client.get(refresh_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_logout_api_get_not_allowed(self, authenticated_client, logout_url):
        response = authenticated_client.get(logout_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_logout_all_devices_api_get_not_allowed(
        self, authenticated_client, logout_all_url
    ):
        response = authenticated_client.get(logout_all_url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
