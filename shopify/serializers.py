from rest_framework import serializers

from .models import (
    Customer, Cart, Wishlist, Product, Category,
    Order, OrderItem, Payment, Shipment
)
import uuid

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Cart
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Wishlist
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    items = OrderItemSerializer(many=True, read_only=True)
    payments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    shipments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Shipment
        fields = '__all__'