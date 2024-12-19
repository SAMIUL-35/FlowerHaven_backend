from rest_framework import viewsets, permissions, filters, pagination
from .models import Flower
from .serializers import FlowerSerializer

class FlowerPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class FlowerViewSet(viewsets.ModelViewSet):
    queryset = Flower.objects.select_related('category').all()
    serializer_class = FlowerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = FlowerPagination
    search_fields = ['name', 'category__name']
    ordering_fields = ['name', 'price']  
    ordering = ['name']  # Default ordering
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Flower.objects.select_related('category').all()
        category = self.request.query_params.get('category')
        if category:
            try:
                category = int(category)
                queryset = queryset.filter(category__id=category)
            except ValueError:
                queryset = Flower.objects.none()
        return queryset
