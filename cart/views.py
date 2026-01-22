from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
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


def cart_update_ajax(request):
    """Update cart quantities via AJAX and return JSON"""
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if product_id:
            cart.update_quantity(product_id, quantity)
            
            # Find the item total for the specific product
            item_total = "0,00"
            for item in cart:
                if str(item['product'].id) == str(product_id):
                    item_total = f"{item['total_price']:.2f}".replace('.', ',')
                    break
            
            return JsonResponse({
                'success': True,
                'item_total': item_total,
                'cart_total': f"{cart.get_total_price():.2f}".replace('.', ','),
                'cart_count': len(cart),
            })
            
    return JsonResponse({'success': False}, status=400)
