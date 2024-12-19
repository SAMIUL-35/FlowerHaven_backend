from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),  # Default Order ViewSet URLs
    path('payment-success/', OrderViewSet.as_view({'post': 'payment_success'}), name='payment-success'),
    # Other paths for payment failure or cancellation can also be added here
]
