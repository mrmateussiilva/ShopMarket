from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('delivery', 'Entrega'),
        ('pickup', 'Retirada'),
    ]
    
    PAYMENT_CHOICES = [
        ('online', 'Online'),
        ('on_delivery', 'Na Entrega'),
        ('in_store', 'Na Retirada'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('preparing', 'Preparando'),
        ('ready', 'Pronto'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name="Usuário"
    )
    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        verbose_name="Método de Entrega"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name="Método de Pagamento"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )
    
    # Totals
    products_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total de Produtos"
    )
    discount_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Total de Desconto"
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Subtotal"
    )
    
    # Delivery info
    delivery_address = models.TextField(blank=True, verbose_name="Endereço de Entrega")
    delivery_notes = models.TextField(blank=True, verbose_name="Observações")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Pedido"
    )
    product_name = models.CharField(max_length=200, verbose_name="Nome do Produto")
    product_code = models.CharField(max_length=50, verbose_name="Código do Produto")
    quantity = models.PositiveIntegerField(verbose_name="Quantidade")
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Unitário"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Total"
    )

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
