from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Cart, Flower
from .serializers import CartSerializer



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        flower_id = self.request.data.get('flower_id')
        quantity = self.request.data.get('quantity', 1)

        try:
            flower = Flower.objects.get(id=flower_id)
        except Flower.DoesNotExist:
            raise Response({'error': 'Flower not found'}, status=status.HTTP_404_NOT_FOUND)
        
        instance, created = Cart.objects.get_or_create(user=self.request.user, flower=flower)
        if not created:
            instance.quantity += int(quantity)
        else:
            instance.quantity = int(quantity)
        instance.save()

        serializer.save()
