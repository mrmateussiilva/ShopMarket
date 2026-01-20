from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    image = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name="Imagem")
    link = models.URLField(blank=True, verbose_name="Link")
    order = models.IntegerField(default=0, verbose_name="Ordem")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['order']

    def __str__(self):
        return self.title
