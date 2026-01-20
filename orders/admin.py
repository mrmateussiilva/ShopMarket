from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_code', 'quantity', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'store', 'status', 'delivery_method', 'payment_method', 'subtotal', 'created_at']
    list_filter = ['status', 'delivery_method', 'payment_method', 'store']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['products_total', 'discount_total', 'subtotal', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('user', 'store', 'status')
        }),
        ('Entrega e Pagamento', {
            'fields': ('delivery_method', 'payment_method', 'delivery_address', 'delivery_notes')
        }),
        ('Totais', {
            'fields': ('products_total', 'discount_total', 'subtotal')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'unit_price', 'total_price']
    search_fields = ['product_name', 'product_code']
