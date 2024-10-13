from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/push/', views.push_product, name='push_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
]