from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from django.db.models import Sum

import uuid

from .models import (
    Customer, Cart, Wishlist, Product, Category,
    Order, OrderItem, Payment, Shipment
)
from .serializers import (
    CustomerSerializer, CartSerializer, WishlistSerializer, ProductSerializer,
    CategorySerializer, OrderSerializer, OrderItemSerializer,
    PaymentSerializer, ShipmentSerializer
)


# --------------------
# CRUD Views
# --------------------

# Customer
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Cart
class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# Wishlist
class WishlistListCreateView(generics.ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

class WishlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

# Product
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Category
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
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

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

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

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

# Payment
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Shipment
class ShipmentListCreateView(generics.ListCreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


# ----------------------------
# Analytics View
# ----------------------------

class SalesAnalyticsView(APIView):
    def get(self, request):
        today = now().date()
        last_30_days = today - timedelta(days=30)

        total_orders = Order.objects.count()
        total_sales = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0

        monthly_orders = Order.objects.filter(created_at__gte=last_30_days)
        monthly_sales = monthly_orders.aggregate(total=Sum('total_amount'))['total'] or 0

        top_products = OrderItem.objects.values('product__name').annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:5]

        top_customers = Customer.objects.annotate(
            total_spent=Sum('orders__total_amount')
        ).order_by('-total_spent')[:5]

        return Response({
            "total_orders": total_orders,
            "total_sales": total_sales,
            "monthly_sales": monthly_sales,
            "top_products": list(top_products),
            "top_customers": [
                {
                    "name": f"{c.first_name} {c.last_name}",
                    "email": c.email,
                    "spent": c.total_spent
                }
                for c in top_customers
            ]
        })
