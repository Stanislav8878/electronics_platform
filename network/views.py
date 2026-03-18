"""Представления API для работы с сетью электроники."""
from rest_framework import viewsets

from .filters import NetworkNodeFilter
from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD для продуктов."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ('name', 'model')
    ordering_fields = ('id', 'name', 'release_date')


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """CRUD для звеньев сети/поставщиков с фильтрацией по стране."""

    queryset = NetworkNode.objects.select_related('supplier').prefetch_related('products').all()
    serializer_class = NetworkNodeSerializer
    filterset_class = NetworkNodeFilter
    search_fields = ('name', 'email', 'country', 'city')
    ordering_fields = ('id', 'name', 'created_at', 'debt_to_supplier')
