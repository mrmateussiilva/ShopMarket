from django.db import models
from decimal import Decimal
from catalog.models import Product
from stores.models import Store


class ProductPrice(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name="Produto"
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='prices',
        verbose_name="Loja"
    )
    regular_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço Regular"
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Preço Promocional"
    )
    club_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Preço Clube"
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Preço do Produto"
        verbose_name_plural = "Preços dos Produtos"
        unique_together = ['product', 'store']
        ordering = ['product__name']

    def __str__(self):
        return f"{self.product.name} - {self.store.name} - R$ {self.get_best_price()}"

    def get_best_price(self):
        """Retorna o melhor preço disponível"""
        if self.club_price:
            return self.club_price
        if self.sale_price:
            return self.sale_price
        return self.regular_price

    def get_discount_percentage(self):
        """Calcula a porcentagem de desconto"""
        if self.sale_price and self.sale_price < self.regular_price:
            discount = ((self.regular_price - self.sale_price) / self.regular_price) * 100
            return int(discount)
        return 0

    def has_discount(self):
        """Verifica se há desconto"""
        return self.get_discount_percentage() > 0
