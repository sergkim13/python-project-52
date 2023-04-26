from django.forms import ModelForm

from .constants import NAME
from .models import Label


class LabelForm(ModelForm):

    class Meta:
        model = Label
        fields = (NAME,)
