"""Фильтры для API."""
import django_filters

from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    """Фильтр для выборки звеньев сети по стране."""

    country = django_filters.CharFilter(field_name="country", lookup_expr="iexact")

    class Meta:
        """Настройки фильтра."""

        model = NetworkNode
        fields = ("country",)
