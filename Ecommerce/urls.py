"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shopify import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', views.CustomerListCreateView.as_view(), name='customer-list-create'),
    path('carts/', views.CartListCreateView.as_view(), name='cart-list-create'),
    path('wishlists/', views.WishlistListCreateView.as_view(), name='wishlist-list-create'),    
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('order-items/', views.OrderItemListCreateView.as_view(), name='order-item-list-create'),
    path('payments/', views.PaymentListCreateView.as_view(), name='payment-list-create'),
    path('shipments/', views.ShipmentListCreateView.as_view(), name='shipment-list-create'),
    
]
