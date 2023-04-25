from django.urls import URLPattern, path

from .constants import CREATE_LABEL, DELETE_LABEL, LIST_LABELS, UPDATE_LABEL
from .views import LabelCreateView, LabelDeleteView, LabelListView, LabelUpdateView

urlpatterns: list[URLPattern] = [
    path('', LabelListView.as_view(), name=LIST_LABELS),
    path('create/', LabelCreateView.as_view(), name=CREATE_LABEL),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name=UPDATE_LABEL),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name=DELETE_LABEL),
]
