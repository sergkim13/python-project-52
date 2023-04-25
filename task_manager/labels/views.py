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
    LABEL_USED_IN_TASK,
    MSG_CREATED,
    MSG_DELETED,
    MSG_UPDATED,
    REVERSE_LABELS,
)
from .forms import LabelForm
from .models import Label


class LabelListView(AuthRequiredMixin, ListView):
    '''Show the list of labels.'''
    model: type[Label] = Label
    context_object_name: str = 'labels'
    extra_context: dict = CONTEXT_LIST


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    '''Create label.'''
    model: type[Label] = Label
    extra_context: dict = CONTEXT_CREATE
    form_class: type[BaseForm] = LabelForm
    success_url: str | Callable[..., Any] = REVERSE_LABELS
    success_message: str = MSG_CREATED


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    '''Update label.'''
    model: type[Label] = Label
    extra_context: dict = CONTEXT_UPDATE
    form_class: type[BaseForm] = LabelForm
    success_url: str | Callable[..., Any] = REVERSE_LABELS
    success_message: str = MSG_UPDATED


class LabelDeleteView(AuthRequiredMixin, DeletionProtectionMixin, SuccessMessageMixin):
    '''Delete label.'''
    model: type[Label] = Label
    context_object_name: str = 'label'
    extra_content: dict = CONTEXT_DELETE
    success_url: str | Callable[..., Any] = REVERSE_LABELS
    success_message: str = MSG_DELETED
    protected_data_url: str | Callable[..., Any] = REVERSE_LABELS
    protected_data_message: str = LABEL_USED_IN_TASK
