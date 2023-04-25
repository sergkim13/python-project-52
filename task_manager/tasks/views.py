from typing import Any, Callable

from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.tasks.filters import TasksFilter

from ..mixins import AuthorDeletionPermissionMixin, AuthRequiredMixin
from .constants import (
    CONTEXT_CREATE,
    CONTEXT_DELETE,
    CONTEXT_DETAIL,
    CONTEXT_LIST,
    CONTEXT_UPDATE,
    MSG_CREATED,
    MSG_DELETED,
    MSG_NOT_AUTHOR_FOR_DELETE_TASK,
    MSG_UPDATED,
    REVERSE_TASKS,
)
from .forms import TaskForm
from .models import Task


class TaskDetailView(AuthRequiredMixin, DetailView):
    '''Show info about specific task.'''
    model: type[Task] = Task
    extra_context: dict = CONTEXT_DETAIL


class TaskListView(AuthRequiredMixin, FilterView):
    '''Show the list of tasks.'''
    model: type[Task] = Task
    context_object_name: str = 'tasks'
    extra_context: dict = CONTEXT_LIST
    filterset_class: type[TasksFilter] = TasksFilter


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    '''Create task.'''
    model: type[Task] = Task
    extra_context: dict = CONTEXT_CREATE
    form_class: type[BaseForm] = TaskForm
    success_url: str | Callable[..., Any] = REVERSE_TASKS
    success_message: str = MSG_CREATED

    def form_valid(self, form):
        '''Auto fill in `author` field with current user.'''
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    '''Update task.'''
    model: type[Task] = Task
    extra_context: dict = CONTEXT_UPDATE
    form_class: type[BaseForm] = TaskForm
    success_url: str | Callable[..., Any] = REVERSE_TASKS
    success_message: str = MSG_UPDATED


class TaskDeleteView(AuthRequiredMixin, AuthorDeletionPermissionMixin, SuccessMessageMixin, DeleteView):
    '''Delete tasks.'''
    model: type[Task] = Task
    context_object_name: str = 'task'
    extra_content: dict = CONTEXT_DELETE
    success_url: str | Callable[..., Any] = REVERSE_TASKS
    success_message: str = MSG_DELETED
    unpermission_message: str = MSG_NOT_AUTHOR_FOR_DELETE_TASK
    unpermission_url: str = REVERSE_TASKS
