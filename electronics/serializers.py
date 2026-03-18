"""Serializers for the electronics API."""
from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """Read-only representation of products linked to a network node."""

    class Meta:
        """Serializer settings."""

        model = Product
        fields = ('id', 'name', 'model', 'release_date')


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Serializer for network node CRUD operations."""

    products = ProductSerializer(many=True, read_only=True)
    hierarchy_level = serializers.IntegerField(read_only=True)

    class Meta:
        """Serializer settings."""

        model = NetworkNode
        fields = (
            'id',
            'entity_type',
            'name',
            'email',
            'country',
            'city',
            'street',
            'house_number',
            'supplier',
            'debt',
            'created_at',
            'hierarchy_level',
            'products',
        )
        read_only_fields = ('created_at', 'hierarchy_level', 'products')

    def get_fields(self):
        """Make debt read-only on updates while allowing it on create."""
        fields = super().get_fields()
        request = self.context.get('request')
        if self.instance is not None or (request and request.method in ('PUT', 'PATCH')):
            fields['debt'].read_only = True
        return fields
