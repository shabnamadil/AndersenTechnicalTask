from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tasks.models import Task

from .permissions import IsAuthenticatedReadOnlyOrAuthor
from .repositories import TaskRepository
from .serializers import TaskListSerializer, TaskPostSerializer


class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticated,)
    repo = TaskRepository

    def get_serializer_class(self):
        if self.request.method == "POST":
            self.serializer_class = TaskPostSerializer
        return super().get_serializer_class()

    def get_filter_methods(self):
        repo = self.repo()
        return {
            "status": repo.get_by_status,
            "q": repo.get_by_query,
        }

    def get_queryset(self, **kwargs):
        qs = Task.objects.all()
        filters = self.get_filter_methods()

        for key, value in self.request.query_params.items():
            if key in filters:
                qs = filters[key](value, qs)
        return qs


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskListSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticatedReadOnlyOrAuthor,)


class MarkTaskCompletedView(APIView):
    permission_classes = (IsAuthenticatedReadOnlyOrAuthor,)
    repo = TaskRepository

    def post(self, request, pk):
        task = self.repo.mark_task_completed(pk, request.user)
        if not task:
            return Response({"detail": "Task not found"}, status=404)
        if task.status == Task.Status.COMPLETED:
            return Response({"status": "already completed"}, status=200)
        return Response({"status": "completed"}, status=200)
