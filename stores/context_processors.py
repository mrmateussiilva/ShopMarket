from .models import ShopConfig
from catalog.models import Category


def shop_config(request):
    """Disponibiliza a configuração da loja em todos os templates"""
    return {
        'shop': ShopConfig.get_config(),
        'categories': Category.objects.filter(is_active=True, parent__isnull=True),
    }
