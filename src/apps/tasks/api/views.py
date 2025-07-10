from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from .permissions import IsTaskAuthor
from .serializers import (
    TaskListSerializer,
    TaskPostSerializer
)

from apps.tasks.models import Task
from .repositories import TaskRepository


class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticated, IsTaskAuthor)
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
        qs = Task.objects.filter(user=self.request.user)
        filters = self.get_filter_methods()

        for key, value in self.request.query_params.items():
            if key in filters:
                qs = filters[key](value, qs)
        return qs
    

class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticated, IsTaskAuthor)
    

class MarkTaskCompletedView(APIView):
    permission_classes = (IsAuthenticated, IsTaskAuthor)
    repo = TaskRepository

    def post(self, request, pk):
        task = self.repo.mark_task_completed(pk, request.user)
        if not task:
            return Response({"detail": "Task not found"}, status=404)
        if task.status == Task.Status.COMPLETED:
            return Response({"status": "already completed"}, status=200)
        return Response({"status": "completed"}, status=200)