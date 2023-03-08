from django.urls import path, URLPattern
from typing import List

from .views import UsersListView #, UserCreateView, UserUpdateView, UserDeleteView


urlpatterns: List[URLPattern] = [
    path('', UsersListView.as_view(), name='users_list'),
    # path('create/', UserCreateView.as_view(), name=CREATE_USER),
    # path('<int:pk>/update/', UserUpdateView.as_view(), name=UPDATE_USER),
    # path('<int:pk>/delete/', UserDeleteView.as_view(), name=DELETE_USER)
]