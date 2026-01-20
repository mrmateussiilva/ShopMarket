from django.contrib import admin
from .models import ProductPrice


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'store', 'regular_price', 'sale_price', 'club_price', 'is_active']
    list_filter = ['is_active', 'store']
    search_fields = ['product__name', 'store__name']
    autocomplete_fields = ['product', 'store']
