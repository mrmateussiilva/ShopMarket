from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Categoria Pai"
    )
    description = models.TextField(blank=True, verbose_name="Descrição")
    is_active = models.BooleanField(default=True, verbose_name="Ativa")
    order = models.IntegerField(default=0, verbose_name="Ordem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['order', 'name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Categoria"
    )
    description = models.TextField(blank=True, verbose_name="Descrição")
    unit = models.CharField(max_length=20, default="un", verbose_name="Unidade")
    is_featured = models.BooleanField(default=False, verbose_name="Destaque")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    image = models.ImageField(upload_to='products/main/', blank=True, null=True, verbose_name="Imagem Principal")


    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Produto"
    )
    image = models.ImageField(upload_to='products/', verbose_name="Imagem")
    is_primary = models.BooleanField(default=False, verbose_name="Imagem Principal")
    order = models.IntegerField(default=0, verbose_name="Ordem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens dos Produtos"
        ordering = ['-is_primary', 'order']

    def __str__(self):
        return f"{self.product.name} - Imagem {self.id}"
