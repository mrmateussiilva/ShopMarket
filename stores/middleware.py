from django.shortcuts import redirect
from django.urls import reverse


class StoreMiddleware:
    """Middleware to ensure a store is selected"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Paths that don't require store selection
        self.exempt_paths = [
            '/admin/',
            '/accounts/',
            '/select-store/',
            '/static/',
            '/media/',
        ]

    def __call__(self, request):
        # Check if path is exempt
        path = request.path
        is_exempt = any(path.startswith(exempt) for exempt in self.exempt_paths)
        
        # If not exempt and no store selected, redirect to store selection
        if not is_exempt and 'store_id' not in request.session:
            if path != reverse('select_store'):
                return redirect('select_store')
        
        response = self.get_response(request)
        return response
