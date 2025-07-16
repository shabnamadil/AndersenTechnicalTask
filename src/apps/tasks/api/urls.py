from django.urls import path

from .views import (
    MarkTaskCompletedView,
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("tasks/", TaskListCreateAPIView.as_view(), name="tasks"),
    path(
        "tasks/<int:pk>/",
        TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task_update_destroy",
    ),
    path(
        "tasks/<int:pk>/completed/",
        MarkTaskCompletedView.as_view(),
        name="task_completed",
    ),
]
