import uuid
import json
import pytest
from django.urls import reverse
from django.test import Client
from shopify.models import Product, Customer, Order, Cart, Shipment, Payment

@pytest.mark.django_db
def test_product_to_order_flow():
    client = Client()

    # Create a customer with unique email
    email = f"test_{uuid.uuid4()}@example.com"
    customer = Customer.objects.create(name="Test User", email=email)

    # Create a product with proper SKU length
    product = Product.objects.create(
        name='Test Product',
        price=10.0,
        stock=5,
        sku=str(uuid.uuid4())[:30]  # Truncate to 30 chars
    )

    # Add product to cart
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

    # Place order
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
    print("Order creation response:", response.json())
    assert response.status_code in [200, 201], f"Place order failed: {response.status_code}, {response.content}"
    
    # Get order UUID from response
    order_data = response.json()
    order_uuid = order_data.get('uuid')
    assert order_uuid is not None, "No UUID found in order response"
    
    # Verify order was created using UUID
    assert Order.objects.filter(uuid=order_uuid).exists(), "Order not found in database"

    # Create payment for the order
    place_payment_url = reverse('payment-list-create')
    response = client.post(
        place_payment_url,
        data=json.dumps({
            'order': order_uuid,  # Use UUID here
            'amount': 20.0,
            'payment_method': 'Credit Card',
            'status': 'Completed'
        }),
        content_type='application/json'
    )
    assert response.status_code in [200, 201], f"Payment creation failed: {response.status_code}, {response.content}"
    payment_data = response.json()
    payment_uuid = payment_data.get('uuid') or payment_data.get('id')
    assert payment_uuid is not None, "Payment ID not returned"

    # Create shipment for the order
    place_shipment_url = reverse('shipment-list-create')
    response = client.post(
        place_shipment_url,
        data=json.dumps({
            'order': order_uuid,  # Use UUID here
            'tracking_number': str(uuid.uuid4()),
            'carrier': 'DHL',
            'status': 'Shipped'
        }),
        content_type='application/json'
    )
    assert response.status_code in [200, 201], f"Shipment creation failed: {response.status_code}, {response.content}"
    shipment_data = response.json()
    shipment_uuid = shipment_data.get('uuid') or shipment_data.get('id')
    assert shipment_uuid is not None, "Shipment ID not returned"

    # Final verification
    order = Order.objects.get(uuid=order_uuid)  # Get by UUID
    assert float(order.total_amount) == 20.0  # Convert to float for Decimal comparison
    assert order.customer == customer

    payment = Payment.objects.get(uuid=payment_uuid) if hasattr(Payment, 'uuid') else Payment.objects.get(id=payment_uuid)
    assert float(payment.amount) == 20.0
    assert payment.status == 'Completed'

    shipment = Shipment.objects.get(uuid=shipment_uuid) if hasattr(Shipment, 'uuid') else Shipment.objects.get(id=shipment_uuid)
    assert shipment.status == 'Shipped'

    print("Test completed successfully: Product to Order flow verified.")