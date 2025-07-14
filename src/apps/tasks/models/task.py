from django.contrib.auth import get_user_model
from django.db import models

from utils.models.base_model import BaseModel

User = get_user_model()


class Task(BaseModel):

    class Status(models.TextChoices):
        NEW = "New", "New"
        IN_PROGRESS = "In progress", "In progress"
        COMPLETED = "Completed", "Completed"

    title = models.CharField(
        "Title",
        max_length=100,
        help_text="The content length is a maximum of 100.",
    )
    description = models.TextField("Description", blank=True, null=True)
    status = models.CharField(
        "Status", max_length=11, choices=Status.choices, default=Status.NEW
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Author",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["-created_at"])]
        unique_together = ("user", "title")
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self) -> str:
        return self.title
