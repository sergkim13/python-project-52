from typing import Any, Callable

from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.constants import REVERSE_LOGIN

from ..mixins import DeletionProtectionMixin, ModifyPermissionMixin
from .constants import (
    CONTEXT_CREATE,
    CONTEXT_DELETE,
    CONTEXT_LIST,
    CONTEXT_UPDATE,
    MSG_DELETED,
    MSG_REGISTERED,
    MSG_UNPERMISSION_TO_MODIFY,
    MSG_UPDATED,
    REVERSE_USERS,
    USER_USED_IN_TASK,
)
from .forms import UserForm
from .models import User


class UserListView(ListView):
    '''Show the list of users.'''
    model: type[User] = User
    context_object_name: str = 'users'
    extra_context: dict = CONTEXT_LIST


class UserCreateView(SuccessMessageMixin, CreateView):
    '''Create user.'''
    model: type[User] = User
    extra_context: dict = CONTEXT_CREATE
    form_class: type[BaseForm] = UserForm
    success_url: str | Callable[..., Any] = REVERSE_LOGIN
    success_message: str = MSG_REGISTERED


class UserUpdateView(ModifyPermissionMixin, SuccessMessageMixin, UpdateView):
    '''Update user.'''
    model: type[User] = User
    extra_context: dict = CONTEXT_UPDATE
    form_class: type[BaseForm] = UserForm
    success_url: str | Callable[..., Any] = REVERSE_USERS
    success_message: str = MSG_UPDATED
    unpermission_url: str | Callable[..., Any] = REVERSE_USERS
    unpermission_message: str = MSG_UNPERMISSION_TO_MODIFY


class UserDeleteView(DeletionProtectionMixin, ModifyPermissionMixin, SuccessMessageMixin, DeleteView):
    '''Delete user.'''
    model: type[User] = User
    context_object_name: str = 'user'
    extra_content: dict = CONTEXT_DELETE
    success_url: str | Callable[..., Any] = REVERSE_USERS
    success_message: str = MSG_DELETED
    unpermission_url: str | Callable[..., Any] = REVERSE_USERS
    unpermission_message: str = MSG_UNPERMISSION_TO_MODIFY
    protected_data_url: str | Callable[..., Any] = REVERSE_USERS
    protected_data_message: str = USER_USED_IN_TASK
