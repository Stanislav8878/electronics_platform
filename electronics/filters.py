"""Filter sets for the electronics API."""
import django_filters

from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    """Filter API results by country."""

    country = django_filters.CharFilter(field_name='country', lookup_expr='iexact')

    class Meta:
        """Filter configuration."""

        model = NetworkNode
        fields = ('country',)
