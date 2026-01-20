from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'address']
    prepopulated_fields = {'slug': ('name',)}
