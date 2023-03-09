from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from typing import Dict, Any, Union, Callable, Type

from .models import User
from .forms import UserRegistrationForm # , UserEditingForm
from .constants import REVERSE_USERS, REVERSE_LOGIN, \
    CONTEXT_LIST, CONTEXT_CREATE, CONTEXT_UPDATE, CONTEXT_DELETE, \
    MSG_REGISTERED, MSG_UPDATED, MSG_DELETED, MSG_UNPERMISSION_TO_MODIFY, \
    USER_USED_IN_TASK
# from ..mixins import ModifyPermissionMixin, DeletionProtectionMixin


class UsersListView(ListView):
    '''Show the list of users.'''
    model: type[User] = User
    context_object_name: str = 'users'
    extra_context: dict = CONTEXT_LIST


class UserCreateView(SuccessMessageMixin, CreateView):
    '''Create a user.'''
    model: type[User] = User
    extra_context:dict = CONTEXT_CREATE
    form_class: type[BaseForm] = UserRegistrationForm
    success_url: Union[str, Callable[..., Any]] = REVERSE_LOGIN
    success_message: str = MSG_REGISTERED
