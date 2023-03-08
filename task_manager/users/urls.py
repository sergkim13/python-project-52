from django.urls import URLPattern, path

# , UserCreateView, UserUpdateView, UserDeleteView
from .views import UsersListView

urlpatterns: list[URLPattern] = [
    path('', UsersListView.as_view(), name='users_list'),
    # path('create/', UserCreateView.as_view(), name=CREATE_USER),
    # path('<int:pk>/update/', UserUpdateView.as_view(), name=UPDATE_USER),
    # path('<int:pk>/delete/', UserDeleteView.as_view(), name=DELETE_USER)
]
