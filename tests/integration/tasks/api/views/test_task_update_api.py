from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework import status

from apps.tasks.models import Task

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestTaskUpdateAPI:

    def test_update_task_as_authenticated_author(
        self, authenticated_client, task_detail_url, task
    ):
        response = authenticated_client.patch(
            task_detail_url,
            {"title": "Updated title"},
        )
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.title == "Updated title"

    def test_update_task_as_non_authenticated_author(
        self, api_client, task_detail_url, task
    ):
        response = api_client.patch(
            task_detail_url,
            {"title": "Updated title"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        task.refresh_from_db()
        assert task.title != "Updated title"

    def test_update_task_as_non_author(
        self, api_client, another_user, task_detail_url, task
    ):
        api_client.force_authenticate(user=another_user)
        response = api_client.patch(
            task_detail_url,
            {"title": "Updated title"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        task.refresh_from_db()
        assert task.title != "Updated title"

    def test_update_task_user_not_allowed(
        self, authenticated_client, task, task_detail_url, another_user
    ):
        response = authenticated_client.patch(
            task_detail_url,
            {"user": another_user},
        )
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.user != another_user

    def test_update_task_description_works_correctly(
        self, authenticated_client, task, task_detail_url
    ):
        response = authenticated_client.patch(
            task_detail_url,
            {"description": "Updated description"},
        )
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.description == "Updated description"

    def test_update_task_status_works_correctly(
        self, authenticated_client, task, task_detail_url
    ):
        response = authenticated_client.patch(
            task_detail_url,
            {"status": Task.Status.COMPLETED},
        )
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.status == Task.Status.COMPLETED

    def test_update_nonexistent_task(self, authenticated_client):
        url = reverse("task_update_destroy", args=[9999])
        response = authenticated_client.patch(
            url,
            {"title": "Updated title"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
