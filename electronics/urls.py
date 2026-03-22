"""Маршруты API приложения electronics."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register("nodes", NetworkNodeViewSet, basename="nodes")
router.register("products", ProductViewSet, basename="products")

network_list = NetworkNodeViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

network_detail = NetworkNodeViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("", include(router.urls)),
    path("network/", network_list, name="network-list"),
    path("network/<int:pk>/", network_detail, name="network-detail"),
]