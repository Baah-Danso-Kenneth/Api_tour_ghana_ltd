from .models import LightningPayment, Order, Product

def handle_payment_confirmation(r_hash: str):

    try:
        # Retrieve the LightningPayment record using the r_hash
        payment = LightningPayment.objects.get(r_hash=r_hash)

        # If the payment is already marked as paid, we do nothing
        if payment.is_paid:
            return "Payment already processed."

        # Mark the payment as paid
        payment.is_paid = True
        payment.save()

        # Retrieve the associated order
        order = Order.objects.get(payment=payment)

        # Mark the order as paid
        order.paid = True
        order.save()

        # Update product stock
        product = order.product
        product.stock_quantity -= order.quantity
        product.save()

        return "Payment confirmed and stock updated."

    except LightningPayment.DoesNotExist:
        return "Payment not found."
    except Order.DoesNotExist:
        return "Order not found."
