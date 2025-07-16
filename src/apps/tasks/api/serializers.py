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

    def validate(self, attrs):
        user = self.context["request"].user
        title = attrs.get("title")

        if Task.objects.filter(title=title, user=user).exists():
            raise serializers.ValidationError(
                {"title": "A task with this title already exists for this user."}
            )
        return attrs
