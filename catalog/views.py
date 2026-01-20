from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product
from cms.models import Banner


def home(request):
    """Home page with banners and featured products"""
    banners = Banner.objects.filter(is_active=True)
    
    # Get featured products (products with prices)
    featured_products = Product.objects.filter(
        is_active=True,
        price__is_active=True
    ).select_related('price').distinct()[:12]
    
    # Get products on sale
    sale_products = Product.objects.filter(
        is_active=True,
        price__is_active=True,
        price__sale_price__isnull=False
    ).select_related('price').distinct()[:8]
    
    # Get newest products
    new_products = Product.objects.filter(
        is_active=True,
        price__is_active=True
    ).select_related('price').order_by('-created_at')[:8]
    
    # Get categories
    categories = Category.objects.filter(is_active=True, parent__isnull=True)[:8]
    
    context = {
        'banners': banners,
        'featured_products': featured_products,
        'sale_products': sale_products,
        'new_products': new_products,
        'categories': categories,
    }
    return render(request, 'catalog/home.html', context)


def category_list(request, slug):
    """Category page with products"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Get products in this category and subcategories
    categories = [category]
    categories.extend(category.children.filter(is_active=True))
    
    products = Product.objects.filter(
        is_active=True,
        category__in=categories,
        price__is_active=True
    ).select_related('price', 'category')
    
    # Sorting
    sort = request.GET.get('sort', 'relevancia')
    if sort == 'menor_preco':
        products = products.order_by('price__regular_price')
    elif sort == 'maior_preco':
        products = products.order_by('-price__regular_price')
    elif sort == 'maior_desconto':
        products = products.filter(price__sale_price__isnull=False).order_by('price__sale_price')
    elif sort == 'mais_novos':
        products = products.order_by('-created_at')
    else:  # relevancia
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'sort': sort,
    }
    return render(request, 'catalog/category_list.html', context)


def product_detail(request, slug, pk):
    """Product detail page"""
    product = get_object_or_404(
        Product.objects.select_related('price', 'category'),
        pk=pk,
        slug=slug,
        is_active=True
    )
    
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context)


def search(request):
    """Search products"""
    query = request.GET.get('q', '')
    products = Product.objects.none()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(code__icontains=query),
            is_active=True,
            price__is_active=True
        ).select_related('price', 'category').distinct()
    
    # Sorting
    sort = request.GET.get('sort', 'relevancia')
    if sort == 'menor_preco':
        products = products.order_by('price__regular_price')
    elif sort == 'maior_preco':
        products = products.order_by('-price__regular_price')
    elif sort == 'maior_desconto':
        products = products.filter(price__sale_price__isnull=False).order_by('price__sale_price')
    elif sort == 'mais_novos':
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'sort': sort,
    }
    return render(request, 'catalog/search.html', context)
