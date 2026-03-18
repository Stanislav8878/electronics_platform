"""API routes for the electronics app."""
from rest_framework.routers import DefaultRouter

from .views import NetworkNodeViewSet

router = DefaultRouter()
router.register('nodes', NetworkNodeViewSet, basename='nodes')

urlpatterns = router.urls
