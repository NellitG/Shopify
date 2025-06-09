import django
import os
import uuid
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Ecommerce.settings")
django.setup()

import pytest
from django.urls import reverse
from django.test import Client
from shopify.models import Product, Customer, Order, Cart, Shipment, Payment


@pytest.mark.django_db
def test_product_to_order_flow():
    client = Client()

    #Create a customer
    customer = Customer.objects.create(name="Test User", email="test@example.com")

    #Create a product
    product = Product.objects.create(
        name='Test Product',
        price=10.0,
        stock=5,
        sku=str(uuid.uuid4())
    )

    #Add product to cart
    add_to_cart_url = reverse('cart-list-create')
    response = client.post(
        add_to_cart_url,
        data=json.dumps({
            'customer': customer.id,
            'product': product.id,
            'quantity': 2
        }),
        content_type='application/json'
    )
    assert response.status_code in [200, 201], f"Add to cart failed: {response.status_code}, {response.content}"

    cart_id = response.json().get('id')
    assert cart_id is not None, "Cart ID not returned in response"

    #Place order
    place_order_url = reverse('order-list-create')
    response = client.post(
        place_order_url,
        data=json.dumps({
            'customer': customer.id,
            'cart_id': cart_id,
            'total_amount': 20.0
        }),
        content_type='application/json'
    )
    assert response.status_code in [200, 201], f"Place order failed: {response.status_code}, {response.content}"

    #Verify order was created
    assert Order.objects.exists(), "No order created"

    #Create a payment for the order
    order_id = response.json().get('id')

    place_payment_url = reverse('payment-list-create')
    response = client.post(
        place_payment_url,
        data=json.dumps({
            'order': order_id,
            'amount': 20.0,
            'payment_method': 'Credit Card',
            'status': 'Completed'
        }),
        content_type='application/json'
    )
    assert response.status_code in [200, 201], f"Place payment failed: {response.status_code}, {response.content}"

    #Create a shipment for the order
    payment_id = response.json().get('id')

    place_shipment_url = reverse('shipment-list-create')
    response = client.post(
        place_shipment_url,
        data=json.dumps({
            'order': order_id,
            'tracking_number': str(uuid.uuid4()),
            'carrier': 'DHL',
            'status': 'Shipped'
        }),
        content_type='application/json'
    )
    assert response.status_code in [200, 201], f"Place shipment failed: {response.status_code}, {response.content}" 

    #Final verification: did the order and payment persist?
    assert Order.objects.filter(id=order_id)
    order = Order.objects.get(id=order_id)
    assert order.total_amount == 20.0
    assert order.customer == customer

    payment = Payment.objects.filter(order=order_id).first()
    assert payment is not None, "Payment not created"
    assert payment.amount == 20.0
    assert payment.status == 'Completed'

    print("Test completed successfully: Product to Order flow verified.")
