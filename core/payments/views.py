from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lnd_grpc.lnd_client import create_invoice
from .models import LightningPayment, Order
from .service import handle_payment_confirmation
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Product
import requests


class GenerateInvoiceView(APIView):
    def post(self, request):
        # Extract the amount and memo from the request
        amount_in_sats = request.data.get("amount_in_sats")
        memo = request.data.get("memo", "Invoice for payment")

        # Ensure the amount_in_sats is provided
        if not amount_in_sats:
            return Response({"error": "Amount in sats is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            result = create_invoice(amount_sats=amount_in_sats, memo=memo)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the lightning payment record in the database
        lightning_payment = LightningPayment.objects.create(
            invoice_id=result["r_hash"],
            amount_in_sats=amount_in_sats,
            payment_request=result["payment_request"],
            r_hash=result["r_hash"]
        )

        # Return the response with the payment request and r_hash
        return Response({
            "payment_request": lightning_payment.payment_request,
            "r_hash": lightning_payment.r_hash
        })


class CreateOrderInvoiceView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        if product.stock_quantity < quantity:
            return Response({"error": "Not enough stock."}, status=400)

        total_amount = product.price_in_sats * quantity

        # Generate invoice from helper
        invoice_data = create_invoice(amount_sats=total_amount, memo="Order Payment")
        invoice_id = invoice_data.get("r_hash")

        if not invoice_id:
            return Response({"error": "Invoice generation failed"}, status=500)

        # Save Lightning payment
        payment = LightningPayment.objects.create(
            r_hash=invoice_data["r_hash"],
            invoice_id=invoice_id,
            payment_request=invoice_data["payment_request"],
            amount_in_sats=total_amount,
        )

        # Create the order
        order = Order.objects.create(
            product=product,
            quantity=quantity,
            total_amount_sats=total_amount,
            payment=payment
        )

        return Response({
            "order_id": order.id,
            "payment_request": payment.payment_request
        }, status=201)


class PaymentConfirmationView(APIView):
    def post(self, request):
        r_hash = request.data.get("r_hash")  # r_hash is received from the payment system
        if not r_hash:
            return Response({"error": "Missing r_hash"}, status=400)

        handle_payment_confirmation(r_hash)
        return Response({"message": "Payment processed"}, status=200)
