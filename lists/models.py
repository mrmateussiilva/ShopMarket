from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product


class List(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lists',
        verbose_name="Usuário"
    )
    name = models.CharField(max_length=200, verbose_name="Nome")
    products = models.ManyToManyField(
        Product,
        related_name='lists',
        verbose_name="Produtos"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Lista"
        verbose_name_plural = "Listas"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"
