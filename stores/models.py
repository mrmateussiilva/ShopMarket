from django.db import models
from django.core.exceptions import ValidationError


class ShopConfig(models.Model):
    """Configuração única da loja - Singleton"""
    
    # Informações básicas
    name = models.CharField(max_length=200, verbose_name="Nome da Loja")
    logo = models.ImageField(upload_to='shop/', blank=True, null=True, verbose_name="Logo")
    
    # Contato
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    
    # Endereço
    address = models.TextField(verbose_name="Endereço")
    
    # Horário
    business_hours = models.TextField(
        verbose_name="Horário de Funcionamento",
        help_text="Ex: Seg-Sex: 8h-20h | Sáb: 8h-18h | Dom: 8h-14h"
    )
    
    # Sobre
    about = models.TextField(verbose_name="Sobre a Loja", blank=True)
    
    # Redes sociais
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Configuração da Loja"
        verbose_name_plural = "Configuração da Loja"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Garantir que só existe uma configuração (Singleton)
        if not self.pk and ShopConfig.objects.exists():
            raise ValidationError('Já existe uma configuração de loja. Edite a existente.')
        return super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        """Retorna a configuração da loja (cria se não existir)"""
        config, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'ShopMarket',
                'address': 'Rua Exemplo, 123 - São Paulo/SP',
                'business_hours': 'Seg-Sex: 8h-20h | Sáb: 8h-18h | Dom: 8h-14h',
                'about': 'Seu supermercado online de confiança!',
            }
        )
        return config
