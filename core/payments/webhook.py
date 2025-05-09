import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import LightningPayment, Order


@api_view(['POST'])
@permission_classes([AllowAny])
def lightning_webhook(request):

    auth_header = request.headers.get("X-Webhook-Secret")
    if auth_header != os.getenv("WEBHOOK_SECRET"):
        return Response({"error": "Unauthorized"}, status=403)

    try:
        data = request.data
        r_hash = data.get('r_hash')

        if not r_hash:
            return Response({'error': 'Missing r_hash'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = LightningPayment.objects.get(r_hash=r_hash)
            payment.paid = True
            payment.paid_at = timezone.now()
            payment.save()

            orders = Order.objects.filter(payment=payment)
            if orders.exists():
                order = orders.first()
                order.paid = True
                order.save()

            return Response({'status': 'payment processed'}, status=status.HTTP_200_OK)

        except LightningPayment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
