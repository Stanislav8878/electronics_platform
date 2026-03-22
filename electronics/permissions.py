"""Кастомные права доступа для API."""
from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """Разрешает доступ только активным сотрудникам."""

    def has_permission(self, request, view):
        """Проверяет, что пользователь активен и является сотрудником."""
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)
