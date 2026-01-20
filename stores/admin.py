from django.contrib import admin
from .models import ShopConfig


@admin.register(ShopConfig)
class ShopConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'logo', 'about')
        }),
        ('Contato', {
            'fields': ('whatsapp', 'phone', 'email')
        }),
        ('Localização', {
            'fields': ('address', 'business_hours')
        }),
        ('Redes Sociais', {
            'fields': ('facebook_url', 'instagram_url')
        }),
    )
    
    def has_add_permission(self, request):
        # Só permite adicionar se não existir nenhuma configuração
        return not ShopConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Não permite deletar a configuração
        return False
