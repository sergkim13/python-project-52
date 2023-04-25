from django.urls import URLPattern, path

from .constants import LIST_STATUSES, CREATE_STATUS, UPDATE_STATUS, DELETE_STATUS
from .views import StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView

urlpatterns: list[URLPattern] = [
    path('', StatusListView.as_view(), name=LIST_STATUSES),
    path('create/', StatusCreateView.as_view(), name=CREATE_STATUS),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name=UPDATE_STATUS),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name=DELETE_STATUS),
]
