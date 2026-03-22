"""Представления API."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import NetworkNodeFilter
from .models import NetworkNode, Product
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(ModelViewSet):
    """CRUD-интерфейс для звеньев сети."""

    queryset = NetworkNode.objects.select_related("supplier").all()
    serializer_class = NetworkNodeSerializer
    permission_classes = (IsActiveStaff,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NetworkNodeFilter


class ProductViewSet(ModelViewSet):
    """CRUD-интерфейс для продуктов."""

    queryset = Product.objects.select_related("node").all()
    serializer_class = ProductSerializer
    permission_classes = (IsActiveStaff,)
