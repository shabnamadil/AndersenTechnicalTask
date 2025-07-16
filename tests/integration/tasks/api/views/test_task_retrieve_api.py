from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

import pytest
from freezegun import freeze_time
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestRetrieveAPI:

    def test_retrieve_task_as_authenticated_user(
        self, authenticated_client, task_detail_url, task
    ):
        response = authenticated_client.get(task_detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == task.id

    def test_retrieve_task_as_non_authenticated_user(self, api_client, task_detail_url):
        response = api_client.get(task_detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_task_when_access_token_expired(
        self, api_client, task_detail_url, user, get_access_token
    ):
        now = timezone.now()

        with freeze_time(now):
            token = get_access_token(user)

        with freeze_time(now + timedelta(minutes=6)):
            api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            response = api_client.get(task_detail_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_nonexistent_task(self, authenticated_client):
        url = reverse("task_update_destroy", args=[9999])
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
