"""Права доступа к API."""
from rest_framework.permissions import BasePermission


class IsActiveEmployee(BasePermission):
    """Разрешает доступ только активным сотрудникам.

    Под сотрудником в рамках задания понимается пользователь, который:
    - аутентифицирован,
    - активен,
    - отмечен как staff.
    """

    message = 'Доступ к API разрешен только активным сотрудникам.'

    def has_permission(self, request, view) -> bool:
        """Проверяет, что пользователь активен и является сотрудником."""
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)
