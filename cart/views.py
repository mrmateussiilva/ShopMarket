from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalog.models import Product
from .cart import Cart


def cart_detail(request):
    """Cart detail page"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity)
    messages.success(request, f'{product.name} adicionado ao carrinho!')
    
    # Redirect back to previous page or product detail
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)


def cart_remove(request, product_id):
    """Remove product from cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.success(request, f'{product.name} removido do carrinho!')
    return redirect('cart_detail')


def cart_update(request):
    """Update cart quantities"""
    cart = Cart(request)
    
    for item_id, quantity in request.POST.items():
        if item_id.startswith('quantity_'):
            product_id = item_id.replace('quantity_', '')
            try:
                quantity = int(quantity)
                cart.update_quantity(product_id, quantity)
            except ValueError:
                pass
    
    messages.success(request, 'Carrinho atualizado!')
    return redirect('cart_detail')


def cart_clear(request):
    """Clear the cart"""
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Carrinho limpo!')
    return redirect('cart_detail')
