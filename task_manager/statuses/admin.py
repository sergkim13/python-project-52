from django.contrib import admin

from .models import Status


@admin.register(Status)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'created_at')
    list_filter = (('created_at'),)
