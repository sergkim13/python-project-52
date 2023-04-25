from typing import Any, Callable

from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from django.views.generic import CreateView, ListView, UpdateView

from ..mixins import AuthRequiredMixin, DeletionProtectionMixin
from .constants import (
    CONTEXT_CREATE,
    CONTEXT_DELETE,
    CONTEXT_LIST,
    CONTEXT_UPDATE,
    MSG_CREATED,
    MSG_DELETED,
    MSG_UPDATED,
    REVERSE_STATUSES,
    STATUS_USED_IN_TASK,
)
from .forms import StatusForm
from .models import Status


class StatusListView(AuthRequiredMixin, ListView):
    '''Show the list of statuses.'''
    model: type[Status] = Status
    context_object_name: str = 'statuses'
    extra_context: dict = CONTEXT_LIST


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    '''Create status.'''
    model: type[Status] = Status
    extra_context: dict = CONTEXT_CREATE
    form_class: type[BaseForm] = StatusForm
    success_url: str | Callable[..., Any] = REVERSE_STATUSES
    success_message: str = MSG_CREATED


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    '''Update status.'''
    model: type[Status] = Status
    extra_context: dict = CONTEXT_UPDATE
    form_class: type[BaseForm] = StatusForm
    success_url: str | Callable[..., Any] = REVERSE_STATUSES
    success_message: str = MSG_UPDATED


class StatusDeleteView(AuthRequiredMixin, DeletionProtectionMixin, SuccessMessageMixin):
    '''Delete status.'''
    model: type[Status] = Status
    context_object_name: str = 'status'
    extra_content: dict = CONTEXT_DELETE
    success_url: str | Callable[..., Any] = REVERSE_STATUSES
    success_message: str = MSG_DELETED
    protected_data_url: str | Callable[..., Any] = REVERSE_STATUSES
    protected_data_message: str = STATUS_USED_IN_TASK
