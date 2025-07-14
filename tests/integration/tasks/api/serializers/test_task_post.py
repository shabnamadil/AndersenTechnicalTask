from django.contrib.auth import get_user_model

import pytest

from apps.tasks.api.serializers import TaskPostSerializer
from apps.tasks.models import Task

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestPostSerializer:

    @pytest.mark.parametrize(
        "field, value",
        [("title", ""), ("status", "")],
    )
    def test_missing_required_fields(self, field, value, task_data):
        task_data[field] = value
        serializer = TaskPostSerializer(data=task_data)
        assert not serializer.is_valid()
        assert field in serializer.errors

    def test_title_user_unique_already_created(self, task_data, fake_request):
        Task.objects.create(**task_data)
        serializer = TaskPostSerializer(
            data=task_data, context={"request": fake_request}
        )
        assert not serializer.is_valid(), serializer.errors
        assert "title" in serializer.errors

    def test_serializer_fields(self, task_data):
        serializer = TaskPostSerializer(data=task_data)
        assert set(serializer.fields.keys()) == {
            "id",
            "title",
            "description",
            "status",
            "user",
            "created_date",
        }

    def test_read_only_fields_are_ignored_on_input(self, user, fake_request):
        data = {
            "title": "Test Task",
            "description": "Test Description",
            "status": Task.Status.NEW,
            "user": 999,
            "created_date": "2024-01-01T00:00:00Z",
        }
        serializer = TaskPostSerializer(data=data, context={"request": fake_request})
        assert serializer.is_valid(), serializer.errors
        task = serializer.save(user=user)
        assert task.user == user
        assert task.created_date != "2024-01-01"

    def test_status_field_validation(self, task_data):
        task_data["status"] = "invalid_status"
        serializer = TaskPostSerializer(data=task_data)
        assert not serializer.is_valid()
        assert "status" in serializer.errors

    def test_create_task_with_valid_data(self, task_data, user, fake_request):
        serializer = TaskPostSerializer(
            data=task_data, context={"request": fake_request}
        )
        assert serializer.is_valid(), serializer.errors
        task = serializer.save(user=user)
        assert task.title == task_data["title"]
        assert task.description == task_data["description"]
        assert task.status == task_data["status"]
        assert task.user == user
        assert task.created_date is not None
