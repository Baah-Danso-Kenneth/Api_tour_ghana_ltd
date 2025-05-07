from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from lnd_grpc.lnd_client import create_invoice
from .models import LightningPayment

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
