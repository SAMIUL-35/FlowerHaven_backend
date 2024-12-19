from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlowerViewSet

router = DefaultRouter()
router.register(r'', FlowerViewSet, basename='flower')

urlpatterns = [
    path('', include(router.urls)),
]
