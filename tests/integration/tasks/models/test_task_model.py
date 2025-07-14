from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import pytest

from apps.tasks.models import Task
from tests.factories import TaskFactory, UserFactory

User = get_user_model()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def task():
    return TaskFactory()


@pytest.mark.integration
@pytest.mark.django_db
class TestTaskCreation:

    def test_create_task_with_valid_data(self, task):
        assert task.pk is not None
        assert task.status == Task.Status.NEW
        assert task.title != ""
        assert task.description != ""
        assert task.user is not None

    @pytest.mark.parametrize(
        "field, value",
        [
            ("title", ""),
            ("status", ""),
            ("user", None),
        ],
    )
    def test_required_fields_raise_validation_error(self, task, field, value):
        setattr(task, field, value)
        with pytest.raises(ValidationError):
            task.full_clean()

    def test_create_task_without_description_does_not_raise_error(self, task):
        task.description = ""
        task.full_clean()
        assert task.description == ""

    def test_raises_validation_error_when_invalid_status_choices(self, task):
        task.status = "invalid_status"
        with pytest.raises(ValidationError):
            task.full_clean()

    def test_title_user_uniqueness_together(self, task):
        with pytest.raises(IntegrityError):
            TaskFactory(title=task.title, user=task.user)

    def test_task_user_is_instance_of_custom_user(self, task):
        assert isinstance(task.user, User)

    def test_user_deletion_removes_task(self, task):
        task.user.delete()
        assert Task.objects.count() == 0

    def test_task_status_changes(self, task):
        task.status = Task.Status.COMPLETED
        assert task.status == Task.Status.COMPLETED
