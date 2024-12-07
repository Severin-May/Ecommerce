from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_info', views.billing_info, name='billing_info'),
    path('process_order', views.order_processing, name='process_order'),
    path('orders/<int:pk>', views.orders, name='orders'),
    path('shipped_orders', views.shipped_orders, name='shipped_orders'),
    path('pending_orders', views.pending_orders, name='pending_orders'),
]
