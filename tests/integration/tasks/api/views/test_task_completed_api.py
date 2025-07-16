from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

from apps.tasks.models import Task

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestTaskCompletedAPI:

    def test_complete_task_as_authenticated_user(
        self, authenticated_client, task_complete_url, task, fake_request
    ):
        response = authenticated_client.patch(
            task_complete_url,
            {"status": Task.Status.COMPLETED},
            context={"request": fake_request},
        )
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.status == Task.Status.COMPLETED

    def test_complete_task_as_non_authenticated_user(
        self,
        api_client,
        task_complete_url,
        task,
    ):
        response = api_client.patch(
            task_complete_url,
            {"status": Task.Status.COMPLETED},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        task.refresh_from_db()
        assert task.status != Task.Status.COMPLETED

    def test_complete_task_as_non_author(
        self, api_client, another_user, task_complete_url, task
    ):
        api_client.force_authenticate(user=another_user)
        response = api_client.patch(
            task_complete_url,
            {"status": Task.Status.COMPLETED},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        task.refresh_from_db()
        assert task.status != Task.Status.COMPLETED

    def test_complete_nonexistent_task(self, authenticated_client):
        url = reverse("task_completed", args=[9999])
        response = authenticated_client.patch(
            url,
            {"status": Task.Status.COMPLETED},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
