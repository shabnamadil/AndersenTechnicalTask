from django.contrib.auth import get_user_model

import pytest
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.integration
class TestTaskUpdateAPI:

    def test_update_task_as_authenticated_author(
        self, authenticated_client, task_detail_url, task
    ):
        response = authenticated_client.put(
            task_detail_url,
            {"title": "Updated title"},
        )
        assert response.status_code == status.HTTP_200_OK
        task.refresh_from_db()
        assert task.title == "Updated title"
