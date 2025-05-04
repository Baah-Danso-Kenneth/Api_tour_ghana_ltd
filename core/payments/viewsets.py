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