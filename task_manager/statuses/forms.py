from django import forms
from django.forms import ModelForm

from .constants import NAME, STATUS_NAME, STATUS_NAME_HELP_TEXT
from .models import Status


class StatusForm(ModelForm):
    name = forms.CharField(required=True, label=STATUS_NAME, help_text=STATUS_NAME_HELP_TEXT)

    class Meta:
        model = Status
        fields = (NAME,)
