from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'author', 'executor', 'created_at')
    search_fields = ('name', 'status', 'author', 'executor')
    list_filter = (
        ('created_at'),
        ('author', admin.RelatedOnlyFieldListFilter),
        ('executor', admin.RelatedOnlyFieldListFilter),
        ('status', admin.RelatedOnlyFieldListFilter),
    )
