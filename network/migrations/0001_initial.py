# Generated manually for test assignment.
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('model', models.CharField(max_length=255, verbose_name='Модель')),
                ('release_date', models.DateField(verbose_name='Дата выхода на рынок')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ('name', 'model'),
                'unique_together': {('name', 'model')},
            },
        ),
        migrations.CreateModel(
            name='NetworkNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('country', models.CharField(max_length=128, verbose_name='Страна')),
                ('city', models.CharField(max_length=128, verbose_name='Город')),
                ('street', models.CharField(max_length=255, verbose_name='Улица')),
                ('house_number', models.CharField(max_length=32, verbose_name='Номер дома')),
                ('debt_to_supplier', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, verbose_name='Задолженность перед поставщиком')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('products', models.ManyToManyField(blank=True, related_name='nodes', to='network.product', verbose_name='Продукты')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='network.networknode', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Звено сети',
                'verbose_name_plural': 'Звенья сети',
                'ordering': ('id',),
            },
        ),
    ]
