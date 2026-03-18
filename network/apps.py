"""Конфигурация приложения сети электроники."""
from django.apps import AppConfig


class NetworkConfig(AppConfig):
    """Настройки приложения network."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'network'
    verbose_name = 'Сеть электроники'
