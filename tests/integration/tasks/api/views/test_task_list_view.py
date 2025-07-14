from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

import pytest
from freezegun import freeze_time
from rest_framework import status

from apps.tasks.models import Task
from tests.factories import TaskFactory, UserFactory

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestTaskListAPI:

    def test_get_task_list_as_authenticated_user(
        self, authenticated_client, task_list_create_url
    ):
        response = authenticated_client.get(task_list_create_url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_tasks_without_authentication(self, api_client, task_list_create_url):
        response = api_client.get(task_list_create_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_task_list_with_status_filter(
        self, authenticated_client, task_list_create_url
    ):
        TaskFactory(status=Task.Status.COMPLETED)
        TaskFactory(status=Task.Status.NEW)

        response = authenticated_client.get(
            task_list_create_url, {"status": Task.Status.COMPLETED}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_get_task_list_with_query_filter(
        self, authenticated_client, task_list_create_url, user
    ):
        TaskFactory(title="Buy milk", user=user)
        TaskFactory(title="Buy eggs", user=user)
        TaskFactory(title="Walk the dog", user=user)

        response = authenticated_client.get(task_list_create_url, {"q": "BUY"})
        assert response.status_code == status.HTTP_200_OK

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_get_task_list_with_user_filter(
        self, authenticated_client, task_list_create_url
    ):
        Jhon = UserFactory(first_name="Jhon")
        Doe = UserFactory(first_name="Doe")
        TaskFactory(user=Jhon)
        TaskFactory(user=Doe)

        response = authenticated_client.get(task_list_create_url, {"user": Jhon.id})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_task_list_when_access_token_expired(
        self, api_client, task_list_create_url, user, get_access_token
    ):
        now = timezone.now()

        with freeze_time(now):
            token = get_access_token(user)

        with freeze_time(now + timedelta(minutes=6)):
            api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
            response = api_client.get(task_list_create_url)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
