from django.urls import path
from . import views

urlpatterns = [
    path('carrinho/', views.cart_detail, name='cart_detail'),
    path('carrinho/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('carrinho/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('carrinho/update/', views.cart_update, name='cart_update'),
    path('carrinho/update-ajax/', views.cart_update_ajax, name='cart_update_ajax'),
    path('carrinho/clear/', views.cart_clear, name='cart_clear'),
]
