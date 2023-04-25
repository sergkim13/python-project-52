from django.urls import URLPattern, path

from .constants import CREATE_STATUS, DELETE_STATUS, LIST_STATUSES, UPDATE_STATUS
from .views import StatusCreateView, StatusDeleteView, StatusListView, StatusUpdateView

urlpatterns: list[URLPattern] = [
    path('', StatusListView.as_view(), name=LIST_STATUSES),
    path('create/', StatusCreateView.as_view(), name=CREATE_STATUS),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name=UPDATE_STATUS),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name=DELETE_STATUS),
]
