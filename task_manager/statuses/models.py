from django.db import models
from django.utils.translation import gettext_lazy


class Status(models.Model):
    name = models.CharField(max_length=256, unique=True, blank=False, verbose_name=gettext_lazy('name'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy('created_at'))

    class Meta:
        verbose_name: str = gettext_lazy('status')
        verbose_name_plural: str = gettext_lazy('statuses')

    def __str__(self) -> str:
        return self.name
