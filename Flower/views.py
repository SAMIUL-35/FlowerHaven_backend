from rest_framework import viewsets, permissions
from .models import Flower
from .serializers import FlowerSerializer

class FlowerViewSet(viewsets.ModelViewSet):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
