from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pedidos/', views.order_list, name='order_list'),
    path('pedidos/<int:order_id>/', views.order_detail, name='order_detail'),
    path('pedidos/<int:order_id>/sucesso/', views.order_success, name='order_success'),
    path('pedidos/<int:order_id>/repetir/', views.repeat_order, name='repeat_order'),
]
