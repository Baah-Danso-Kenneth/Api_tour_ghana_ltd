from django.db import models
from core.shops.models import Product

class LightningPayment(models.Model):
    invoice_id = models.CharField(max_length=255, unique=True)
    amount_in_sats = models.PositiveIntegerField()
    payment_request = models.TextField(blank=True, null=True)
    r_hash = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=50, default="lightning")
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invoice: {self.invoice_id} | Paid: {self.paid}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount_sats = models.PositiveIntegerField()
    payment = models.OneToOneField(LightningPayment, on_delete=models.CASCADE, null=True, blank=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"
