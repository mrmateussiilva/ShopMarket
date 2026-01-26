from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='format_price')
def format_price(value):
    """
    Formata um valor numérico para o padrão brasileiro de preço.
    Exemplo: 5.99 -> 5,99
    """
    try:
        # Converte para Decimal se necessário
        if isinstance(value, str):
            value = Decimal(value)
        
        # Formata com 2 casas decimais
        formatted = f"{float(value):.2f}"
        
        # Substitui ponto por vírgula (padrão brasileiro)
        formatted = formatted.replace('.', ',')
        
        return formatted
    except (ValueError, TypeError, AttributeError):
        return value
