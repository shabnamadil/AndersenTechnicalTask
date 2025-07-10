from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
    description = models.TextField(
        "Description",
        blank=True
    )
    status = models.CharField(
        "Status", max_length=11, choices=Status.choices, default=Status.NEW
    )

    slug = models.SlugField(
        "Slug",
        null=True,
        blank=True,
        max_length=500
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

    def __str__(self) -> str:
        return self.title
