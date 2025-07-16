from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken

from apps.tasks.models import Task
from tests.factories import TaskFactory, UserFactory

User = get_user_model()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def another_user():
    return UserFactory()


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        username="testuser",
        first_name="Test",
        last_name="User",
        password="securepassword",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


@pytest.fixture
def register_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "username": "jhon_doe",
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
    }


@pytest.fixture
def register_url():
    return reverse("register")


@pytest.fixture
def refresh_url():
    return reverse("custom_token_refresh")


@pytest.fixture
def obtain_url():
    return reverse("custom_token_obtain_pair")


@pytest.fixture
def logout_url():
    return reverse("logout")


@pytest.fixture
def logout_all_url():
    return reverse("logout_all")


@pytest.fixture
def task_list_create_url():
    return reverse("tasks")


@pytest.fixture
def task_detail_url(task):
    return reverse("task_update_destroy", args=[task.id])


@pytest.fixture
def task_complete_url(task):
    return reverse("task_completed", args=[task.id])


@pytest.fixture
def tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@pytest.fixture
def valid_credentials(user):
    return {"username": user.username, "password": "securepassword"}


@pytest.fixture
def invalid_credentials():
    return {"username": "wronguser", "password": "wrongpass"}


@pytest.fixture
def task(user):
    return TaskFactory(user=user)


@pytest.fixture
def task_data(user):
    return {
        "title": "Test title",
        "description": "Test desc",
        "status": Task.Status.NEW,
        "user": user,
    }


@pytest.fixture
def fake_request(user):
    factory = APIRequestFactory()
    request = factory.post("/fake-url")
    request.user = user
    return request


@pytest.fixture
def get_access_token():
    def _make_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    return _make_token
