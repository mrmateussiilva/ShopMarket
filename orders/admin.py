from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_code', 'quantity', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'delivery_method', 'payment_method', 'subtotal', 'created_at']
    list_filter = ['status', 'delivery_method', 'payment_method']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['products_total', 'discount_total', 'subtotal', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    actions = ['mark_as_confirmed', 'mark_as_preparing', 'mark_as_ready', 'mark_as_delivered', 'mark_as_cancelled']
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('user', 'status')
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

    @admin.action(description='Confirmar selecionados')
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Marcar como Em Preparação')
    def mark_as_preparing(self, request, queryset):
        queryset.update(status='preparing')

    @admin.action(description='Marcar como Pronto')
    def mark_as_ready(self, request, queryset):
        queryset.update(status='ready')

    @admin.action(description='Marcar como Entregue')
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')

    @admin.action(description='Cancelar selecionados')
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'unit_price', 'total_price']
    search_fields = ['product_name', 'product_code']
