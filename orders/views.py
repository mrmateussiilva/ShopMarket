from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.cart import Cart
from stores.models import Store


@login_required
def checkout(request):
    """Checkout page"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Seu carrinho está vazio!')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        payment_method = request.POST.get('payment_method')
        delivery_address = request.POST.get('delivery_address', '')
        delivery_notes = request.POST.get('delivery_notes', '')
        
        # Create order
        store = Store.objects.get(id=request.session.get('store_id'))
        order = Order.objects.create(
            user=request.user,
            store=store,
            delivery_method=delivery_method,
            payment_method=payment_method,
            delivery_address=delivery_address,
            delivery_notes=delivery_notes,
            products_total=cart.get_total_price(),
            discount_total=cart.get_discount(),
            subtotal=cart.get_subtotal(),
        )
        
        # Create order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                product_code=item['code'],
                quantity=item['quantity'],
                unit_price=item['price'],
                total_price=item['total_price'],
            )
        
        # Clear cart
        cart.clear()
        
        messages.success(request, f'Pedido #{order.id} realizado com sucesso!')
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'orders/checkout.html')


@login_required
def order_list(request):
    """List user's orders"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def repeat_order(request, order_id):
    """Repeat an order by adding its items to cart"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = Cart(request)
    
    # Clear current cart
    cart.clear()
    
    # Add order items to cart
    from catalog.models import Product
    for item in order.items.all():
        try:
            # Try to find product by code
            product = Product.objects.get(code=item.product_code, is_active=True)
            cart.add(product, item.quantity)
        except Product.DoesNotExist:
            messages.warning(request, f'Produto {item.product_name} não está mais disponível.')
    
    messages.success(request, 'Itens do pedido adicionados ao carrinho!')
    return redirect('cart_detail')
