from django.forms import ModelForm

from .constants import DESCRIPTION, EXECUTOR, NAME, STATUS
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = (NAME, DESCRIPTION, STATUS, EXECUTOR)
