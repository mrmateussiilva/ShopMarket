from .models import ShopConfig


def shop_config(request):
    """Disponibiliza a configuração da loja em todos os templates"""
    return {
        'shop': ShopConfig.get_config()
    }
