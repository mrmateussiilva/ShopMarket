from django.contrib import admin
from .models import ProductPrice


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'regular_price', 'sale_price', 'club_price', 'is_active']
    list_filter = ['is_active']
    search_fields = ['product__name', 'product__code']
    autocomplete_fields = ['product']
