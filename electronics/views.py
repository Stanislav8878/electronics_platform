"""API views for the electronics app."""
from rest_framework.viewsets import ModelViewSet

from .filters import NetworkNodeFilter
from .models import NetworkNode
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer


class NetworkNodeViewSet(ModelViewSet):
    """CRUD view set for network nodes."""

    queryset = NetworkNode.objects.select_related('supplier').prefetch_related('products').all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaff]
    filterset_class = NetworkNodeFilter
    search_fields = ('name', 'email', 'city', 'country')
    ordering_fields = ('id', 'name', 'created_at', 'debt')