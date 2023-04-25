from django.urls import URLPattern, path

from .constants import CREATE_TASK, DELETE_TASK, DETAIL_TASK, LIST_TASKS, UPDATE_TASK
from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

urlpatterns: list[URLPattern] = [
    path('', TaskListView.as_view(), name=LIST_TASKS),
    path('create/', TaskCreateView.as_view(), name=CREATE_TASK),
    path('<int:pk>/', TaskDetailView.as_view(), name=DETAIL_TASK),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name=UPDATE_TASK),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name=DELETE_TASK),
]
