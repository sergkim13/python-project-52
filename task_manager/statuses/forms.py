from django import forms
from django.forms import BaseForm

from .constants import (
    STATUS_NAME,
    STATUS_NAME_HELP_TEXT,
    NAME,

)
from .models import Status


class StatusForm(BaseForm):
    name = forms.CharField(required=True, label=STATUS_NAME, help_text=STATUS_NAME_HELP_TEXT)

    class Meta:
        model = Status
        fields = (NAME,)
