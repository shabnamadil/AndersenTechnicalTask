from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

import pytest
from freezegun import freeze_time
from rest_framework import status

from apps.tasks.models import Task
from tests.factories import TaskFactory

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestTaskCreateAPI:

    def test_successful_task_post(
        self, authenticated_client, task_list_create_url, task_data
    ):
        response = authenticated_client.post(task_list_create_url, task_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Task.objects.filter(title=task_data["title"]).exists()

    def test_unauthorizied_task_post(self, api_client, task_list_create_url, task_data):
        response = api_client.post(task_list_create_url, task_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_task_post_with_missing_title(
        self, authenticated_client, task_list_create_url, task_data
    ):
        task_data["title"] = ""
        response = authenticated_client.post(task_list_create_url, task_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    def test_task_post_with_invalid_status(
        self, authenticated_client, task_list_create_url, task_data
    ):
        task_data["status"] = "Invalid status"
        response = authenticated_client.post(task_list_create_url, task_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "status" in response.data

    def test_post_with_existing_title_user_together(
        self, authenticated_client, task_list_create_url, task_data
    ):
        TaskFactory(**task_data)
        response = authenticated_client.post(task_list_create_url, task_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_sets_user_field_from_request_user(
        self, authenticated_client, task_data, user, task_list_create_url
    ):
        task_data["user"] = 9999
        response = authenticated_client.post(task_list_create_url, data=task_data)
        task = Task.objects.get(title=task_data["title"])
        assert response.status_code == status.HTTP_201_CREATED
        assert task.user == user

    def test_post_process_when_access_token_expired(
        self, api_client, task_list_create_url, task_data, user, get_access_token
    ):
        now = timezone.now()

        with freeze_time(now):
            token = get_access_token(user)

        with freeze_time(now + timedelta(minutes=6)):
            api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            response = api_client.post(task_list_create_url, task_data)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
