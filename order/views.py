from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Order, Cart
from .serializers import OrderSerializer
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, ordered=True)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Fetch all the cart items that are not yet purchased
        cart_items = Cart.objects.filter(user=request.user, purchased=False)

        # If the cart is empty, raise an error
        if not cart_items.exists():
            raise ValidationError({"detail": "Your cart is empty."})

        # Calculate total price from all cart items
        total_price = sum(item.get_totals() for item in cart_items)

        # Create the Order object
        order = Order.objects.create(
            user=request.user,
            total_price=total_price
        )

        # Link the cart items with the order
        order.cart_items.set(cart_items)  # Set cart items to order
        order.save()  # Save the order after associating the cart items

        # Payment gateway settings
        settings = {
            'store_id': 'flowe675ea7ca09c98',
            'store_pass': 'flowe675ea7ca09c98@ssl',
            'issandbox': True
        }

        sslcz = SSLCOMMERZ(settings)

        # Data to send to the payment gateway
        post_body = {
            'total_amount': total_price,
            'currency': "BDT",
            'tran_id': str(order.id),
            'success_url': "http://localhost:5173/",
            'fail_url': "http://localhost:5173/cart/",
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
            # Create a session with the payment gateway
            response = sslcz.createSession(post_body)
            print(response)

            if response['status'] == 'SUCCESS':
                # Set paymentId and orderId after successful payment session creation
                order.paymentId = response.get('payment_id')  # Payment ID from the response
                order.orderId = response.get('tran_id')      # Transaction ID from SSLCOMMERZ
                order.save()  # Save the order with the updated paymentId and orderId

                
                Cart.objects.filter(user=request.user, purchased=False).update(purchased=True)
                # Cart.objects.filter(user=request.user, purchased=True).delete()
                Order.objects.filter(user=request.user,ordered=False).update(ordered=True)

                # Return the payment gateway URL to redirect the user
                return Response({
                    'redirect_url': response['GatewayPageURL']
                }, status=200)
            else:
                raise ValidationError({"detail": "Payment session creation failed."})

        except Exception as e:
            # Handle any errors that occurred during the payment session creation
            raise ValidationError({"detail": f"Payment gateway error: {str(e)}"})

    @action(detail=False, methods=["get"], url_path="order-total")
    def order_total(self, request):
        # Calculate the grand total of all orders for the user
        orders = self.get_queryset()
        grand_total = sum(order.total_price for order in orders)

        # Return the total of all orders along with the serialized order data
        return Response({
            "orders": OrderSerializer(orders, many=True).data,
            "grand_total": grand_total
        })
