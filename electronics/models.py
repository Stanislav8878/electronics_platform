"""Модели сети электроники."""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class NetworkNode(models.Model):
    """Модель звена сети по продаже электроники."""

    class EntityType(models.TextChoices):
        """Типы звеньев сети."""

        FACTORY = "factory", "Завод"
        RETAIL = "retail", "Розничная сеть"
        ENTREPRENEUR = "entrepreneur", "Индивидуальный предприниматель"

    entity_type = models.CharField(max_length=20, choices=EntityType.choices, verbose_name="Тип звена")
    name = models.CharField(max_length=255, verbose_name="Название")
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=255, verbose_name="Улица")
    house_number = models.CharField(max_length=50, verbose_name="Номер дома")
    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="clients",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Задолженность",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ("id",)

    def __str__(self):
        """Возвращает человекочитаемое имя объекта."""
        return self.name

    @property
    def hierarchy_level(self):
        """Вычисляет уровень иерархии по цепочке поставщиков."""
        level = 0
        supplier = self.supplier
        while supplier:
            level += 1
            supplier = supplier.supplier
        return level

    def clean(self):
        """Проверяет бизнес-ограничения модели."""
        if self.entity_type == self.EntityType.FACTORY and self.supplier:
            raise ValidationError("Завод не может иметь поставщика.")

        if self.supplier == self:
            raise ValidationError("Объект не может ссылаться сам на себя.")

        supplier = self.supplier
        while supplier:
            if supplier == self:
                raise ValidationError("Обнаружен цикл в цепочке поставщиков.")
            supplier = supplier.supplier

        if self.hierarchy_level > 2:
            raise ValidationError("Допустимы только три уровня иерархии: 0, 1 и 2.")


class Product(models.Model):
    """Модель продукта, связанного со звеном сети."""

    node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Звено сети",
    )
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ("id",)

    def __str__(self):
        """Возвращает название продукта с моделью."""
        return f"{self.name} ({self.model})"
