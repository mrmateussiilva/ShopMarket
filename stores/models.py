from django.db import models
from django.utils.text import slugify


class Store(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    address = models.TextField(verbose_name="Endereço")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    is_active = models.BooleanField(default=True, verbose_name="Ativa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
