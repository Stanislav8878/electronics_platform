"""Настройки административной панели."""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import NetworkNode, Product


@admin.action(description='Очистить задолженность перед поставщиком у выбранных объектов')
def clear_debt(modeladmin, request, queryset):
    """Обнуляет задолженность перед поставщиком у выбранных звеньев сети."""
    queryset.update(debt_to_supplier=0)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Администрирование продуктов."""
    list_display = ('id', 'name', 'model', 'release_date')
    search_fields = ('name', 'model')


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Администрирование звеньев сети."""
    list_display = (
        'id',
        'name',
        'hierarchy_name_display',
        'country',
        'city',
        'supplier_link',
        'debt_to_supplier',
        'created_at',
    )
    list_filter = ('city', 'country', 'created_at')
    search_fields = ('name', 'email', 'city', 'country')
    autocomplete_fields = ('supplier', 'products')
    actions = (clear_debt,)
    readonly_fields = ('created_at', 'hierarchy_name_display', 'supplier_admin_link')
    fieldsets = (
        ('Основная информация', {'fields': ('name', 'hierarchy_name_display', 'supplier', 'supplier_admin_link')}),
        ('Контакты', {'fields': ('email', 'country', 'city', 'street', 'house_number')}),
        ('Коммерческие данные', {'fields': ('products', 'debt_to_supplier', 'created_at')}),
    )

    def hierarchy_name_display(self, obj):
        """Показывает тип звена по вычисленному уровню иерархии."""
        return obj.hierarchy_name

    hierarchy_name_display.short_description = 'Уровень'

    def supplier_link(self, obj):
        """Возвращает HTML-ссылку на поставщика для списка объектов."""
        if not obj.supplier_id:
            return '—'
        return format_html('<a href="/admin/network/networknode/{}/change/">{}</a>', obj.supplier_id, obj.supplier.name)

    supplier_link.short_description = 'Поставщик'

    def supplier_admin_link(self, obj):
        """Возвращает ссылку на поставщика на странице редактирования объекта."""
        if not obj.pk or not obj.supplier_id:
            return '—'
        return mark_safe(f'<a href="/admin/network/networknode/{obj.supplier_id}/change/">{obj.supplier.name}</a>')

    supplier_admin_link.short_description = 'Ссылка на поставщика'
