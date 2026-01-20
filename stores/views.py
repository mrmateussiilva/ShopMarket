from django.shortcuts import render, redirect, get_object_or_404
from .models import Store


def select_store(request):
    """View for selecting a store"""
    if request.method == 'POST':
        store_id = request.POST.get('store_id')
        if store_id:
            # Clear cart when changing stores
            if 'cart' in request.session:
                request.session['cart'] = {}
            
            request.session['store_id'] = int(store_id)
            return redirect('home')
    
    stores = Store.objects.filter(is_active=True)
    return render(request, 'stores/select_store.html', {'stores': stores})


def change_store(request):
    """Change the current store"""
    # Clear store from session to force selection
    if 'store_id' in request.session:
        del request.session['store_id']
    return redirect('select_store')
