from .models import Category

def categories_processor(request):
    """
    Make main categories available in all templates
    """
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by('order', 'name')
    return {
        'main_categories': categories
    }
