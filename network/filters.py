"""Фильтры для API."""
import django_filters

from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    """Фильтрация звеньев сети по стране и городу."""

    country = django_filters.CharFilter(field_name='country', lookup_expr='iexact')
    city = django_filters.CharFilter(field_name='city', lookup_expr='iexact')

    class Meta:
        model = NetworkNode
        fields = ('country', 'city')
