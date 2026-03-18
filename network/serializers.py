"""Сериализаторы API приложения сети электроники."""
from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта."""

    class Meta:
        model = Product
        fields = ('id', 'name', 'model', 'release_date')


class NetworkNodeSerializer(serializers.ModelSerializer):
    """Сериализатор звена сети.

    Поле задолженности доступно только для чтения через API, чтобы запретить его изменение.
    """

    level = serializers.IntegerField(read_only=True)
    hierarchy_name = serializers.CharField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = (
            'id',
            'name',
            'email',
            'country',
            'city',
            'street',
            'house_number',
            'products',
            'supplier',
            'debt_to_supplier',
            'created_at',
            'level',
            'hierarchy_name',
        )
        read_only_fields = ('debt_to_supplier', 'created_at', 'level', 'hierarchy_name')

    def update(self, instance, validated_data):
        """Обновляет объект, игнорируя изменение задолженности при обходе read_only-поля."""
        validated_data.pop('debt_to_supplier', None)
        return super().update(instance, validated_data)
