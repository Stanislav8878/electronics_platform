"""Application configuration for the electronics app."""
from django.apps import AppConfig


class ElectronicsConfig(AppConfig):
    """App configuration for the electronics network domain."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'electronics'
