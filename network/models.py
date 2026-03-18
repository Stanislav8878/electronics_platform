"""Модели предметной области сети по продаже электроники."""
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class Product(models.Model):
    """Продукт, который продается в звеньях сети."""

    name = models.CharField('Название', max_length=255)
    model = models.CharField('Модель', max_length=255)
    release_date = models.DateField('Дата выхода на рынок')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('name', 'model')
        unique_together = ('name', 'model')

    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        return f'{self.name} ({self.model})'


class NetworkNode(models.Model):
    """Звено сети продаж электроники с иерархической связью на поставщика."""

    name = models.CharField('Название', max_length=255)
    email = models.EmailField('Email')
    country = models.CharField('Страна', max_length=128)
    city = models.CharField('Город', max_length=128)
    street = models.CharField('Улица', max_length=255)
    house_number = models.CharField('Номер дома', max_length=32)
    products = models.ManyToManyField(Product, verbose_name='Продукты', related_name='nodes', blank=True)
    supplier = models.ForeignKey(
        'self',
        verbose_name='Поставщик',
        related_name='clients',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    debt_to_supplier = models.DecimalField(
        'Задолженность перед поставщиком',
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    created_at = models.DateTimeField('Время создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'
        ordering = ('id',)

    def __str__(self) -> str:
        """Возвращает название звена сети."""
        return self.name

    @property
    def level(self) -> int:
        """Вычисляет уровень иерархии на основании цепочки поставщиков."""
        level = 0
        current_supplier = self.supplier
        visited_ids = {self.pk} if self.pk else set()
        while current_supplier is not None:
            if current_supplier.pk in visited_ids:
                raise ValidationError('Обнаружен циклический граф поставщиков.')
            visited_ids.add(current_supplier.pk)
            level += 1
            current_supplier = current_supplier.supplier
        return level

    @property
    def hierarchy_name(self) -> str:
        """Возвращает человекочитаемое название уровня иерархии."""
        mapping = {
            0: 'Завод',
            1: 'Розничная сеть',
            2: 'Индивидуальный предприниматель',
        }
        return mapping.get(self.level, 'Вне допустимой иерархии')

    def clean(self) -> None:
        """Проверяет корректность иерархии и отсутствие циклических зависимостей."""
        super().clean()
        if self.supplier_id and self.pk and self.supplier_id == self.pk:
            raise ValidationError({'supplier': 'Объект не может ссылаться сам на себя как на поставщика.'})

        if self.supplier is not None:
            supplier_level = self.supplier.level
            if supplier_level >= 2:
                raise ValidationError({'supplier': 'Нельзя выбрать поставщика с уровнем 2. Максимальная глубина сети — 3 уровня.'})

        if self.level > 2:
            raise ValidationError('Допустимо только три уровня иерархии: 0, 1 и 2.')

    def save(self, *args, **kwargs):
        """Сохраняет объект после полной валидации модели."""
        self.full_clean()
        return super().save(*args, **kwargs)
