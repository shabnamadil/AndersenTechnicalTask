from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

from apps.tasks.models import Task

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestTaskDeleteAPI:

    def test_delete_task_as_authenticated_author(
        self, authenticated_client, task_detail_url, task
    ):
        response = authenticated_client.delete(task_detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=task.id).exists()

    def test_delete_task_as_non_authenticated_user(self, api_client, task_detail_url):
        response = api_client.delete(task_detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_task_as_non_author(
        self, api_client, another_user, task_detail_url, task
    ):
        api_client.force_authenticate(user=another_user)
        response = api_client.delete(task_detail_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Task.objects.filter(id=task.id).exists()

    def test_delete_nonexistent_task(self, authenticated_client):
        url = reverse("task_update_destroy", args=[9999])
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
