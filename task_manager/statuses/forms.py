from django.forms import ModelForm

from .constants import NAME
from .models import Status


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = (NAME,)
