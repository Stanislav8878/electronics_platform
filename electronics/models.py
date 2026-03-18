"""Database models for the electronics trading network."""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class NetworkNode(models.Model):
    """A single node in the electronics sales network."""

    class EntityType(models.TextChoices):
        """Allowed node kinds."""

        FACTORY = 'factory', 'Завод'
        RETAIL = 'retail', 'Розничная сеть'
        ENTREPRENEUR = 'entrepreneur', 'Индивидуальный предприниматель'

    entity_type = models.CharField(max_length=20, choices=EntityType.choices, verbose_name='Тип звена')
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=128, verbose_name='Страна')
    city = models.CharField(max_length=128, verbose_name='Город')
    street = models.CharField(max_length=255, verbose_name='Улица')
    house_number = models.CharField(max_length=32, verbose_name='Номер дома')
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='clients',
        null=True,
        blank=True,
        verbose_name='Поставщик',
    )
    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Задолженность перед поставщиком',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'
        ordering = ('id',)

    def __str__(self) -> str:
        """Return a human-readable object representation."""
        return self.name

    @property
    def hierarchy_level(self) -> int:
        """Compute the level in the supplier chain."""
        level = 0
        current = self.supplier
        seen = set()
        while current is not None:
            if current.pk in seen:
                break
            seen.add(current.pk)
            level += 1
            current = current.supplier
        return level

    def clean(self) -> None:
        """Validate that the node fits into the allowed three-level hierarchy."""
        if self.entity_type == self.EntityType.FACTORY and self.supplier is not None:
            raise ValidationError({'supplier': 'Завод не может иметь поставщика.'})

        if self.supplier_id and self.pk and self.supplier_id == self.pk:
            raise ValidationError({'supplier': 'Объект не может ссылаться сам на себя.'})

        level = 0
        current = self.supplier
        seen = {self.pk} if self.pk else set()
        while current is not None:
            if current.pk in seen:
                raise ValidationError({'supplier': 'Обнаружен цикл в иерархии поставщиков.'})
            seen.add(current.pk)
            level += 1
            if level > 2:
                raise ValidationError({'supplier': 'Допустима иерархия только из трех уровней.'})
            current = current.supplier

    def save(self, *args, **kwargs) -> None:
        """Validate the object before saving it to the database."""
        self.full_clean()
        super().save(*args, **kwargs)


class Product(models.Model):
    """A product sold by a network node."""

    node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='products', verbose_name='Звено сети')
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    def __str__(self) -> str:
        """Return a human-readable product representation."""
        return f'{self.name} ({self.model})'
