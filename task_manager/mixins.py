from typing import Any, Callable

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import DeleteView

from .constants import MSG_NO_PERMISSION, REVERSE_HOME, REVERSE_LOGIN


class AuthRequiredMixin(LoginRequiredMixin):
    '''Sets access rules for unauthenticated users.'''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, MSG_NO_PERMISSION)
            return redirect(REVERSE_LOGIN)

        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    '''Sets access rules for an unauthorized user.'''

    unpermission_message: str = 'Access denied message'
    unpermission_url: str | Callable[..., Any] = REVERSE_LOGIN

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.unpermission_message)
        return redirect(self.unpermission_url)


class DeletionProtectionMixin(DeleteView):
    '''Sets the rules for handling the case of the impossibility of deleting data
    due to the protection of related data.'''

    protected_data_message: str = 'Entity deletion forbidden message'
    protected_data_url: str | Callable[..., Any] = REVERSE_HOME

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        '''Sends data to the server with protection check.'''
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, self.protected_data_message)
            return redirect(self.protected_data_url)


class AuthorDeletionPermissionMixin(UserPassesTestMixin):
    unpermission_message: str = 'Task deletion forbidden message'
    unpermission_url: str = 'redirected_url'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.unpermission_message)
        return redirect(self.unpermission_url)
