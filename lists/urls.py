from django.urls import path
from . import views

urlpatterns = [
    path('listas/', views.list_view, name='list_view'),
    path('listas/criar/', views.list_create, name='list_create'),
    path('listas/<int:list_id>/', views.list_detail, name='list_detail'),
    path('listas/<int:list_id>/add/<int:product_id>/', views.list_add_product, name='list_add_product'),
    path('listas/<int:list_id>/remove/<int:product_id>/', views.list_remove_product, name='list_remove_product'),
    path('listas/<int:list_id>/delete/', views.list_delete, name='list_delete'),
    path('listas/add-quick/<int:product_id>/', views.list_add_product_quick, name='list_add_product_quick'),
]
