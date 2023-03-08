# from django.shortcuts import render
from django.views.generic import ListView

from .constants import CONTEXT_LIST
from .models import User


class UsersListView(ListView):
    '''Show the list of users.'''
    model: type[User] = User
    context_object_name: str = 'users'
    extra_context: dict = CONTEXT_LIST
