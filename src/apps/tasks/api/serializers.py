from rest_framework import serializers
from apps.tasks.models import Task


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status"
        )


class TaskPostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created_date = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "user",
            "created_date"
        )

    def validate(self, attrs):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("You have to log in")
        attrs["user"] = request.user
        return attrs