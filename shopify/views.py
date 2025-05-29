from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.exceptions import ValidationError
from .models import (
    Customer, Cart, Wishlist, Product, Category,
    Order, OrderItem, Payment, Shipment
)
from .serializers import (
    CustomerSerializer, CartSerializer, WishlistSerializer, ProductSerializer,
    CategorySerializer, OrderSerializer, OrderItemSerializer,
    PaymentSerializer, ShipmentSerializer
)
import uuid


# Customer
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Cart
class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# Wishlist
class WishlistListCreateView(generics.ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

# Product
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Category
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Order
class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_id = self.request.query_params.get('customer_id')
        
        if customer_id:
            try:
                customer_uuid = uuid.UUID(customer_id)
            except ValueError:
                raise ValidationError({'customer_id': 'Invalid UUID format'})
            
            queryset = queryset.filter(customer_id=customer_uuid)
        
        return queryset

# OrderItem
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        order_id = self.request.query_params.get('order_id')

        if order_id:
            try:
                order_uuid = uuid.UUID(order_id)
            except ValueError:
                raise ValidationError({'order_id': 'Invalid UUID format'})
            queryset = queryset.filter(order_id=order_uuid)

        return queryset

# Payment
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Shipment
class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
