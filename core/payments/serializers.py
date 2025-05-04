from rest_framework import serializers
from .models import LightningPayment, Order
import uuid


class LightningPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=LightningPayment
        fields = ['invoice_id', 'amount_in_sats', 'paid', 'created_at', 'paid_at', 'payment_type']
        read_only_fields = ['invoice_id', 'paid', 'created_at', 'paid_at']



class OrderSerializer(serializers.ModelSerializer):
    payment = LightningPaymentSerializer()

    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'total_amount_sats', 'payment', 'paid', 'created_at']

    def create(self, validated_data):
        payment_data = validated_data.pop('payment')

        lightning_payment = LightningPayment.objects.create(
                invoice_id=f"inv_{uuid.uuid4().hex[:10]}",
                **payment_data
            )
        order = Order.objects.create(payment=lightning_payment)
        return order