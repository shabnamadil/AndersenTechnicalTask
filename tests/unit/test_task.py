from django.contrib.auth import get_user_model

import pytest

from apps.tasks.models import Task

User = get_user_model()


@pytest.mark.unit
class TestTaskModel:
    def test_title_field_max_length(self):
        field = Task._meta.get_field("title")
        assert field.max_length == 100

    def test_status_field_max_length(self):
        field = Task._meta.get_field("status")
        assert field.max_length == 11

    def test_title_required(self):
        field = Task._meta.get_field("title")
        assert not field.blank
        assert not field.null

    def test_description_field_blank(self):
        field = Task._meta.get_field("description")
        assert field.blank is True
        assert field.null is True

    def test_user_field_relationship(self):
        field = Task._meta.get_field("user")
        assert field.related_model == User
        assert field.remote_field.on_delete.__name__ == "CASCADE"
        assert field.remote_field.related_name == "tasks"

    def test_verbose_name_meta(self):
        assert Task._meta.verbose_name == "Task"
        assert Task._meta.verbose_name_plural == "Tasks"

    def test_str_method_returns_title(self, mocker):
        task = Task(title="Test Task")
        assert str(task) == "Test Task"

    def test_is_completed_returns_true_for_completed_status(self):
        task = Task(status=Task.Status.COMPLETED)
        assert task.status == "Completed"

    def test_model_meta_ordering(self):
        assert Task._meta.ordering == ["-created_at"]

    def test_model_meta_unique_together(self):
        assert ("user", "title") in Task._meta.unique_together
