from django.urls import URLPattern, path

from .constants import CREATE_USER, DELETE_USER, LIST_USERS, UPDATE_USER
from .views import UserCreateView, UserDeleteView, UsersListView, UserUpdateView

urlpatterns: list[URLPattern] = [
    path('', UsersListView.as_view(), name=LIST_USERS),
    path('create/', UserCreateView.as_view(), name=CREATE_USER),
    path('<int:pk>/update/', UserUpdateView.as_view(), name=UPDATE_USER),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name=DELETE_USER),
]
