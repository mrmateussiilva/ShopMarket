from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('c/<slug:slug>/', views.category_list, name='category_list'),
    path('p/<slug:slug>/<int:pk>/', views.product_detail, name='product_detail'),
]
