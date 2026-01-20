from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product
from pricing.models import ProductPrice
from cms.models import Banner


def home(request):
    """Home page with banners and featured products"""
    store_id = request.session.get('store_id')
    banners = Banner.objects.filter(is_active=True)
    
    # Get featured products (products with prices in current store)
    featured_products = Product.objects.filter(
        is_active=True,
        prices__store_id=store_id,
        prices__is_active=True
    ).distinct()[:12]
    
    # Get prices for featured products
    for product in featured_products:
        try:
            product.price = ProductPrice.objects.get(
                product=product,
                store_id=store_id,
                is_active=True
            )
        except ProductPrice.DoesNotExist:
            product.price = None
    
    context = {
        'banners': banners,
        'featured_products': featured_products,
    }
    return render(request, 'catalog/home.html', context)


def category_list(request, slug):
    """Category page with products"""
    store_id = request.session.get('store_id')
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Get products in this category and subcategories
    categories = [category]
    categories.extend(category.children.filter(is_active=True))
    
    products = Product.objects.filter(
        is_active=True,
        category__in=categories,
        prices__store_id=store_id,
        prices__is_active=True
    ).distinct()
    
    # Sorting
    sort = request.GET.get('sort', 'name')
    if sort == 'price_asc':
        products = products.order_by('prices__regular_price')
    elif sort == 'price_desc':
        products = products.order_by('-prices__regular_price')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get prices for products
    for product in page_obj:
        try:
            product.price = ProductPrice.objects.get(
                product=product,
                store_id=store_id,
                is_active=True
            )
        except ProductPrice.DoesNotExist:
            product.price = None
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'sort': sort,
    }
    return render(request, 'catalog/category_list.html', context)


def product_detail(request, slug, pk):
    """Product detail page"""
    store_id = request.session.get('store_id')
    product = get_object_or_404(Product, pk=pk, slug=slug, is_active=True)
    
    # Get price for current store
    try:
        price = ProductPrice.objects.get(
            product=product,
            store_id=store_id,
            is_active=True
        )
    except ProductPrice.DoesNotExist:
        price = None
    
    context = {
        'product': product,
        'price': price,
    }
    return render(request, 'catalog/product_detail.html', context)
