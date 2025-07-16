from django.db.models import Q

from rest_framework.exceptions import PermissionDenied

from apps.tasks.models import Task


class TaskRepository:

    def __init__(self):
        self.model = Task

    def get_by_status(self, status, qs):
        return qs.filter(status=status)

    def get_by_query(self, query, qs):
        return qs.filter(Q(title__contains=query) | Q(description__contains=query))

    def get_by_user(self, user_id, qs):
        return qs.filter(user=user_id)

    def mark_task_completed(task_id, user):
        task = Task.objects.filter(pk=task_id).first()

        if not task:
            return None

        if task.user != user:
            raise PermissionDenied("You do not have permission to modify this task.")

        if task.status != Task.Status.COMPLETED:
            task.status = Task.Status.COMPLETED
            task.save(update_fields=["status"])

        return task
