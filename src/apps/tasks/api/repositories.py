from django.db.models import Q

from apps.tasks.models import Task


class TaskRepository:

    def __init__(self):
        self.model = Task

    @staticmethod
    def mark_task_completed(task_id, user):
        task = Task.objects.filter(pk=task_id, owner=user).first()
        if task and task.status != Task.Status.COMPLETED:
            task.status = Task.Status.COMPLETED
            task.save(update_fields=["status"])
        return task

    def get_by_status(self, status, qs):
        return qs.filter(status=status)

    def get_by_query(self, query, qs):
        return qs.filter(
            Q(title__contains=query)
            | Q(description__contains=query)
        )
