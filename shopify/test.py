import unittest

from django.apps import apps
from django.contrib import admin
from .models import (
    Customer, Category, Product, Cart, CartItem,
    Wishlist, Order, OrderItem, Payment, Shipment
)
from shopify.views import (
    Customer as CustomerView,
    Category as CategoryView,
    Product as ProductView,
    Cart as CartView,
    Wishlist as WishlistView,
    Order as OrderView,
    OrderItem as OrderItemView,
    Payment as PaymentView,
    Shipment as ShipmentView
)

from shopify.serializers import (
    CustomerSerializer, CategorySerializer, ProductSerializer,
    CartSerializer, WishlistSerializer, OrderSerializer,
    OrderItemSerializer, PaymentSerializer, ShipmentSerializer
)
import Ecommerce

class TestUrls(unittest.TestCase):
    def test_urls(self):
        self.assertTrue(hasattr(Ecommerce.urls, 'urlpatterns'))

class TestSettings(unittest.TestCase):
    def test_debug(self):
        self.assertTrue(getattr(Ecommerce.settings, 'DEBUG', False))

    def test_installed_apps(self):
        self.assertIn('shopify', Ecommerce.settings.INSTALLED_APPS)

    def test_middleware(self):
        self.assertIn('django.middleware.common.CommonMiddleware', Ecommerce.settings.MIDDLEWARE)

    def test_database_config(self):
        self.assertIn('default', Ecommerce.settings.DATABASES)
        self.assertEqual(Ecommerce.settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')

class TestSerializers(unittest.TestCase):
    def test_customer_serializer(self):
        self.assertTrue(callable(CustomerSerializer))

    def test_category_serializer(self):
        self.assertTrue(callable(CategorySerializer))

    def test_product_serializer(self):
        self.assertTrue(callable(ProductSerializer))

    def test_cart_serializer(self):
        self.assertTrue(callable(CartSerializer))

    def test_wishlist_serializer(self):
        self.assertTrue(callable(WishlistSerializer))

    def test_order_serializer(self):
        self.assertTrue(callable(OrderSerializer))

    def test_order_item_serializer(self):
        self.assertTrue(callable(OrderItemSerializer))

    def test_payment_serializer(self):
        self.assertTrue(callable(PaymentSerializer))

    def test_shipment_serializer(self):
        self.assertTrue(callable(ShipmentSerializer))


class TestViews(unittest.TestCase):
    def test_customer_view(self):
        self.assertTrue(callable(CustomerView))

    def test_category_view(self):
        self.assertTrue(callable(CategoryView))

    def test_product_view(self):
        self.assertTrue(callable(ProductView))

    def test_cart_view(self):
        self.assertTrue(callable(CartView))

    def test_wishlist_view(self):
        self.assertTrue(callable(WishlistView))

    def test_order_view(self):
        self.assertTrue(callable(OrderView))

    def test_order_item_view(self):
        self.assertTrue(callable(OrderItemView))

    def test_payment_view(self):
        self.assertTrue(callable(PaymentView))

    def test_shipment_view(self):
        self.assertTrue(callable(ShipmentView))

class TestShopifyAdmin(unittest.TestCase):
    def test_admin_registration(self):
        # Check if the models are registered in the admin site
        self.assertIn(Customer, admin.site._registry)
        self.assertIn(Category, admin.site._registry)
        self.assertIn(Product, admin.site._registry)
        self.assertIn(Cart, admin.site._registry)
        self.assertIn(CartItem, admin.site._registry)
        self.assertIn(Wishlist, admin.site._registry)
        self.assertIn(Order, admin.site._registry)
        self.assertIn(OrderItem, admin.site._registry)
        self.assertIn(Payment, admin.site._registry)
        self.assertIn(Shipment, admin.site._registry)

class TestShopifyAppConfig(unittest.TestCase):
    def test_app_config(self):
        app_config = apps.get_app_config('shopify')
        self.assertEqual(app_config.name, 'shopify')

class TestShopifyApp(unittest.TestCase):
    def test_placeholder(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()