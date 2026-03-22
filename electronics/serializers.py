"""Сериализаторы приложения electronics."""
from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта."""

    class Meta:
        """Метаданные сериализатора продукта."""

        model = Product
        fields = ("id", "node", "name", "model", "release_date")


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Сериализатор звена сети."""

    products = ProductSerializer(many=True, read_only=True)
    hierarchy_level = serializers.IntegerField(read_only=True)

    class Meta:
        """Метаданные сериализатора звена сети."""

        model = NetworkNode
        fields = (
            "id",
            "entity_type",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "debt",
            "created_at",
            "hierarchy_level",
            "products",
        )
        read_only_fields = ("created_at", "hierarchy_level", "products")

    def update(self, instance, validated_data):
        """Запрещает обновление задолженности через API."""
        validated_data.pop("debt", None)
        return super().update(instance, validated_data)
