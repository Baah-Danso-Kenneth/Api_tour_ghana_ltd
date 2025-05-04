from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Order, LightningPayment
from .serializers import OrderSerializer, LightningPaymentSerializer

class LightningPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    You probably want LightningPayment to be read-only from the API,
    since it's generated internally when an order is created.
    """
    queryset = LightningPayment.objects.all()
    serializer_class = LightningPaymentSerializer


class OrderViewSet(viewsets.ModelViewSet):
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
