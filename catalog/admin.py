from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage
from pricing.models import ProductPrice


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductPriceInline(admin.StackedInline):
    model = ProductPrice
    can_delete = False
    verbose_name = "Preço"
    verbose_name_plural = "Configuração de Preço"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'order']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'code', 'category', 'unit', 'get_price', 'is_featured', 'is_active']
    list_filter = ['is_active', 'is_featured', 'category']
    search_fields = ['name', 'code']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductPriceInline, ProductImageInline]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Imagem'

    def get_price(self, obj):
        try:
            return f"R$ {obj.price.regular_price}"
        except ProductPrice.DoesNotExist:
            return "-"
    get_price.short_description = 'Preço (R$)'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'order']
    list_filter = ['is_primary']
