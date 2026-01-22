from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.cart import Cart


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
        cash_change = request.POST.get('cash_change')
        
        cart_total = cart.get_total_price()
        
        # Validation for Cash payment
        change_amount = None
        if payment_method == 'money':
            try:
                if cash_change:
                    change_amount = float(cash_change.replace(',', '.'))
                    if change_amount < float(cart_total):
                        messages.error(request, f'O valor do troco (R$ {change_amount:.2f}) deve ser maior ou igual ao total do pedido (R$ {cart_total:.2f}).')
                        return redirect('checkout')
                else:
                    messages.error(request, 'Informe o valor para troco.')
                    return redirect('checkout')
            except ValueError:
                messages.error(request, 'Valor de troco inválido.')
                return redirect('checkout')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            delivery_method=delivery_method,
            payment_method=payment_method,
            delivery_address=delivery_address,
            delivery_notes=delivery_notes,
            products_total=cart.get_total_price(),
            discount_total=cart.get_discount(),
            subtotal=cart.get_subtotal(),
            cash_change=change_amount
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
        
        return redirect('order_success', order_id=order.id)
    
    return render(request, 'orders/checkout.html')


@login_required
def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


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
