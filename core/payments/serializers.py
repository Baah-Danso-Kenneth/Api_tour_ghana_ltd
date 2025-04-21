from rest_framework import serializers
from .models import LightningPayment, Order
import uuid


class LightningPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=LightningPayment
        invoice_id = f"inv_{uuid.uuid4().hex[:10]}"
        fields = ['invoice_id', 'amount_in_sats', 'paid', 'created_at', 'paid_at', 'payment_type']



class OrderSerializer(serializers.ModelSerializer):
    payment = LightningPaymentSerializer()

    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'total_amount_sats', 'payment', 'paid', 'created_at']