import os

from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Order, LightningPayment
from .serializers import OrderSerializer, LightningPaymentSerializer
from rest_framework.permissions import BasePermission
from lnd_grpc.lnd_client import create_invoice


class HashLightningAPIKey(BasePermission):
    def has_permission(self, request, view):
        expected_key = os.getenv("LIGHTNING_API_KEY")
        auth = request.headers.get("Authorization")
        return auth == f"Bearer {expected_key}"
    pass


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [HashLightningAPIKey]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create to catch serializer validation errors cleanly.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LightningPaymentViewSet(viewsets.ModelViewSet):
    queryset = LightningPayment.objects.all()
    serializer_class = LightningPaymentSerializer