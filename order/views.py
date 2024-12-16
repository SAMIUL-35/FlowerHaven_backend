from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Order
from .serializers import OrderSerializer
from cart.models import Cart
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from sslcommerz_lib import SSLCOMMERZ

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user, purchased=False)

        if not cart_items:
            raise ValidationError({"detail": "Your cart is empty."})

        total_price = sum(item.get_totals() for item in cart_items)

        order = Order.objects.create(
            user=request.user,
            total_price=total_price
        )

        order.cart_items.set(cart_items)

        settings = {
            'store_id': 'flowe675ea7ca09c98', 
            'store_pass': 'flowe675ea7ca09c98@ssl',
            'issandbox': True
        }

        sslcz = SSLCOMMERZ(settings)
        post_body = {
            'total_amount': total_price,
            'currency': "BDT",
            'tran_id': str(order.id),
            'success_url': "http://localhost:5173/order",
            'fail_url': "http://localhost:5173/cart",
            'cancel_url': "http://localhost:5173/cart",
            'emi_option': 0,
            'cus_name': request.user.get_full_name(),
            'cus_email': request.user.email,
            'cus_phone': "01678610000",
            'cus_add1': "shahenbag",
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': len(cart_items),
            'product_name': "Test Product",
            'product_category': "Test Category",
            'product_profile': "general"
        }

        try:
            response = sslcz.createSession(post_body)
            print(response)

            if response['status'] == 'SUCCESS':
                return Response({
                    'redirect_url': response['GatewayPageURL']
                }, status=200)
            else:
                raise ValidationError({"detail": "Payment session creation failed."})
        
        except Exception as e:
            raise ValidationError({"detail": f"Payment gateway error: {str(e)}"})

    @action(detail=False, methods=["get"], url_path="order-total")
    def order_total(self, request):
        orders = self.get_queryset()
        grand_total = sum(order.total_price for order in orders)

        return Response({
            "orders": OrderSerializer(orders, many=True).data,
            "grand_total": grand_total
        })
