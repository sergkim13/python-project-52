from django.urls import URLPattern, path

# , UserCreateView, UserUpdateView, UserDeleteView
from .views import UsersListView, UserCreateView
from .constants import CREATE_USER, LIST_USERS

urlpatterns: list[URLPattern] = [
    path('', UsersListView.as_view(), name=LIST_USERS),
    path('create/', UserCreateView.as_view(), name=CREATE_USER),
    # path('<int:pk>/update/', UserUpdateView.as_view(), name=UPDATE_USER),
    # path('<int:pk>/delete/', UserDeleteView.as_view(), name=DELETE_USER)
]
