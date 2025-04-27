from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Order, LightningPayment
from .serializers import OrderSerializer, LightningPaymentSerializer


class LightningPaymentViewset(viewsets.ModelViewSet):
    queryset= LightningPayment.objects.all()
    serializer_class = LightningPaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Extract order and payment data from the request
        order_data = request.data.get('order')
        lightning_payment_data = order_data.get('payment')

        # Create Lightning Payment (dynamically generate invoice_id in a real-world scenario)
        lightning_payment = LightningPayment.objects.create(
            invoice_id="unique_invoice_id",  # Dynamic generation required here
            amount_in_sats=lightning_payment_data['amount_in_sats'],
            payment_type=lightning_payment_data['payment_type'],
        )

        # Create Order
        order = Order.objects.create(
            product_id=order_data['product'],  # Assuming product ID is passed in the data
            quantity=order_data['quantity'],
            total_amount_sats=order_data['total_amount_sats'],
            payment=lightning_payment
        )

        # Return the created order as a response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
