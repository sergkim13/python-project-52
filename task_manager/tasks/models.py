from django.db import models
from django.utils.translation import gettext_lazy

from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=256, verbose_name=gettext_lazy('name'))
    description = models.TextField(verbose_name=gettext_lazy('description'), max_length=5000)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name=gettext_lazy('status'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=gettext_lazy('author'),
                               related_name='author_id')
    executor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=gettext_lazy('executor'),
                                 related_name='executor_id', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy('created_at'))

    class Meta:
        verbose_name: str = gettext_lazy('task')
        verbose_name_plural: str = gettext_lazy('tasks')

    def __str__(self) -> str:
        return self.name
