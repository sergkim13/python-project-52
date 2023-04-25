from django import forms
from django.forms import ModelForm

from .constants import NAME
from .models import Label


class LabelForm(ModelForm):
    name = forms.CharField(required=True)

    class Meta:
        model = Label
        fields = (NAME,)
