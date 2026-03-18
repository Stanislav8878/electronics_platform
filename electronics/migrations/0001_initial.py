# Generated manually for the test task.
from decimal import Decimal

from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    """Initial schema for the electronics network."""

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='NetworkNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_type', models.CharField(choices=[('factory', 'Завод'), ('retail', 'Розничная сеть'), ('entrepreneur', 'Индивидуальный предприниматель')], max_length=20, verbose_name='Тип звена')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('country', models.CharField(max_length=128, verbose_name='Страна')),
                ('city', models.CharField(max_length=128, verbose_name='Город')),
                ('street', models.CharField(max_length=255, verbose_name='Улица')),
                ('house_number', models.CharField(max_length=32, verbose_name='Номер дома')),
                ('debt', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Задолженность перед поставщиком')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='electronics.networknode', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Звено сети',
                'verbose_name_plural': 'Звенья сети',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('model', models.CharField(max_length=255, verbose_name='Модель')),
                ('release_date', models.DateField(verbose_name='Дата выхода на рынок')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='electronics.networknode', verbose_name='Звено сети')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('id',),
            },
        ),
    ]
