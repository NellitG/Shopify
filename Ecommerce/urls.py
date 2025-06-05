from django.contrib import admin
from django.urls import path, include
from shopify import views
from shopify.views import SalesAnalyticsView


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
    path('analytics/sales/', SalesAnalyticsView.as_view(), name='sales-analytics'),
    
]
