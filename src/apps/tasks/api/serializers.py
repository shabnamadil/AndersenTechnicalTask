from rest_framework import serializers

from apps.tasks.models import Task


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "created_date")


class TaskPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        read_only_fields = ("user", "created_date")
        fields = (
            "id",
            "title",
            "description",
            "status",
            "user",
            "created_date",
        )
