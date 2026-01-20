from django.contrib import admin
from .models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name', 'user__username']
    filter_horizontal = ['products']
