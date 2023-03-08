from django.shortcuts import render
from django.views.generic import ListView
from typing import Type, Dict
from .models import User
from .constants import CONTEXT_LIST

class UsersListView(ListView):
    '''Show the list of users.'''
    model: Type[User] = User
    context_object_name: str = 'users'
    extra_context: Dict = CONTEXT_LIST
