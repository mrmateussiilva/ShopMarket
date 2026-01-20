from django.urls import path
from . import views

urlpatterns = [
    path('select-store/', views.select_store, name='select_store'),
    path('change-store/', views.change_store, name='change_store'),
]
