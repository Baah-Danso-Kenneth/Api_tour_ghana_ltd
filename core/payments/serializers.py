from rest_framework import serializers
from .models import LightningPayment, Order
from lnd_grpc.lnd_client import create_invoice
import uuid


class LightningPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=LightningPayment
        fields = ['invoice_id', 'amount_in_sats', 'paid', 'created_at', 'paid_at', 'payment_type', 'payment_request']
        read_only_fields = ['invoice_id', 'paid', 'created_at', 'paid_at', 'payment_request']



class OrderSerializer(serializers.ModelSerializer):
    payment = LightningPaymentSerializer()

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'quantity', 'total_amount_sats',
            'payment', 'paid', 'created_at'
        ]

    def validate(self, attrs):
        payment_data = attrs.get('payment')

        if not payment_data:
            raise serializers.ValidationError({
                'payment': 'This field is required.'
            })

        if 'amount_in_sats' not in payment_data:
            raise serializers.ValidationError({
                'payment': {'amount_in_sats': 'This field is required.'}
            })

        return attrs

    def create(self, validated_data):
        payment_data = validated_data.pop('payment')

        memo = f"Purchase of product #{validated_data.get('product')} x{validated_data.get('quantity')}"
        invoice_data = create_invoice(
            amount_sats= create_invoice(
                amount_sats=payment_data['amount_in_sats'],
                memo=memo
            )
        )

        lightning_payment = LightningPayment.objects.create(
            invoice_id=invoice_data['r_hash'],
            amount_in_sats=payment_data['amount_in_sats'],
            payment_request=invoice_data['payment_request'],
            r_hash=invoice_data['r_hash'],
        )

        order = Order.objects.create(payment=lightning_payment, **validated_data)
        return order
