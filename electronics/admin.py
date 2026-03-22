"""Настройки административной панели."""
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import NetworkNode, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    """Сбрасывает задолженность у выбранных объектов."""
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Административное представление звеньев сети."""

    list_display = ("name", "entity_type", "city", "supplier_link", "hierarchy_level_display", "debt", "created_at")
    list_filter = ("city",)
    search_fields = ("name", "city", "country", "email")
    actions = (clear_debt,)

    def supplier_link(self, obj):
        """Возвращает HTML-ссылку на поставщика."""
        if not obj.supplier:
            return "-"
        url = reverse("admin:electronics_networknode_change", args=[obj.supplier.pk])
        return format_html('<a href="{}">{}</a>', url, obj.supplier.name)

    supplier_link.short_description = "Поставщик"

    def hierarchy_level_display(self, obj):
        """Отображает вычисленный уровень иерархии."""
        return obj.hierarchy_level

    hierarchy_level_display.short_description = "Уровень иерархии"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Административное представление продуктов."""

    list_display = ("name", "model", "node", "release_date")
    list_select_related = ("node",)
    search_fields = ("name", "model")
