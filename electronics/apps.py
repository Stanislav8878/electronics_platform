"""Конфигурация приложения electronics."""
from django.apps import AppConfig


class ElectronicsConfig(AppConfig):
    """Конфигурация приложения сети электроники."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "electronics"
