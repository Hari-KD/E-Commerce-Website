from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard_view, name='admin_dashboard'),
    path('products/', views.manage_products_view, name='manage_products'),
    path('orders/', views.manage_orders_view, name='manage_orders'),
    path('users/', views.manage_users_view, name='manage_users'),
]
