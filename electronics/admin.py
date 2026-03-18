"""Admin configuration for the electronics app."""
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from .models import NetworkNode, Product


@admin.action(description='Очистить задолженность перед поставщиком')
def clear_debt(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet) -> None:
    """Set debt to zero for selected network nodes."""
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Admin for network nodes."""

    list_display = ('id', 'name', 'entity_type', 'city', 'country', 'supplier_link', 'debt', 'hierarchy_level_display', 'created_at')
    list_filter = ('city', 'country', 'entity_type', 'created_at')
    search_fields = ('name', 'email', 'city', 'country')
    readonly_fields = ('created_at', 'hierarchy_level_display')
    actions = (clear_debt,)
    fieldsets = (
        ('Основное', {'fields': ('entity_type', 'name', 'supplier')}),
        ('Контакты', {'fields': ('email', 'country', 'city', 'street', 'house_number')}),
        ('Финансы', {'fields': ('debt',)}),
        ('Служебное', {'fields': ('hierarchy_level_display', 'created_at')}),
    )

    @admin.display(description='Поставщик')
    def supplier_link(self, obj: NetworkNode) -> str:
        """Render a clickable supplier link in the admin list page."""
        if not obj.supplier:
            return '-'
        url = reverse('admin:electronics_networknode_change', args=[obj.supplier.pk])
        return format_html('<a href="{}">{}</a>', url, obj.supplier.name)

    @admin.display(description='Уровень иерархии')
    def hierarchy_level_display(self, obj: NetworkNode) -> int:
        """Expose the computed hierarchy level in the admin interface."""
        return obj.hierarchy_level


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for products."""

    list_display = ('id', 'name', 'model', 'node', 'release_date')
    list_filter = ('release_date', 'node__city')
    search_fields = ('name', 'model', 'node__name')
