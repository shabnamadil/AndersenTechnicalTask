from django.contrib.auth import get_user_model

import pytest

from apps.tasks.api.serializers import TaskListSerializer
from apps.tasks.models import Task
from tests.factories import TaskFactory

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestListSerializer:

    def test_serializer_fields_are_expected(self):
        task = TaskFactory()
        data = TaskListSerializer(task).data
        assert set(data.keys()) == {
            "id",
            "title",
            "description",
            "status",
            "created_date",
        }

    def test_task_serialization(self, task):
        serializer = TaskListSerializer(instance=task)
        data = serializer.data

        assert data["id"] == task.id
        assert data["title"] == task.title
        assert data["description"] == task.description
        assert data["status"] == Task.Status.NEW
        assert data["created_date"] == task.created_date

    def test_task_list_serializer_with_multiple_tasks(self):
        tasks = TaskFactory.create_batch(3)
        serializer = TaskListSerializer(tasks, many=True)
        data = serializer.data

        assert len(data) == 3
        for i, task_data in enumerate(data):
            task = tasks[i]
            assert task_data["id"] == task.id
            assert task_data["title"] == task.title
