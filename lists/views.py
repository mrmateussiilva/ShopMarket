from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import List
from catalog.models import Product


@login_required
def list_view(request):
    """View user's lists"""
    lists = List.objects.filter(user=request.user)
    return render(request, 'lists/list_view.html', {'lists': lists})


@login_required
def list_detail(request, list_id):
    """View list detail"""
    list_obj = get_object_or_404(List, id=list_id, user=request.user)
    return render(request, 'lists/list_detail.html', {'list': list_obj})


@login_required
def list_create(request):
    """Create a new list"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            list_obj = List.objects.create(user=request.user, name=name)
            messages.success(request, f'Lista "{name}" criada com sucesso!')
            return redirect('list_detail', list_id=list_obj.id)
    
    return render(request, 'lists/list_create.html')


@login_required
def list_add_product(request, list_id, product_id):
    """Add product to list"""
    list_obj = get_object_or_404(List, id=list_id, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    
    list_obj.products.add(product)
    messages.success(request, f'{product.name} adicionado à lista {list_obj.name}!')
    
    # Redirect back to previous page
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)


@login_required
def list_remove_product(request, list_id, product_id):
    """Remove product from list"""
    list_obj = get_object_or_404(List, id=list_id, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    
    list_obj.products.remove(product)
    messages.success(request, f'{product.name} removido da lista!')
    
    return redirect('list_detail', list_id=list_id)


@login_required
def list_delete(request, list_id):
    """Delete a list"""
    list_obj = get_object_or_404(List, id=list_id, user=request.user)
    name = list_obj.name
    list_obj.delete()
    messages.success(request, f'Lista "{name}" excluída!')
@login_required
def list_add_product_quick(request, product_id):
    """Add product to the first available list or create one if none exists"""
    product = get_object_or_404(Product, id=product_id)
    
    # Try to find the first list
    list_obj = List.objects.filter(user=request.user).first()
    
    if not list_obj:
        # Create a default list
        list_obj = List.objects.create(user=request.user, name='Minha Lista')
        messages.info(request, 'Criamos a sua "Minha Lista" automaticamente.')
    
    list_obj.products.add(product)
    messages.success(request, f'{product.name} adicionado à sua lista!')
    
    # Redirect back to where we came from
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)
