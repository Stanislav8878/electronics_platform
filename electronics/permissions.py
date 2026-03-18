"""Permission classes for the electronics API."""
from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """Allow access only for authenticated active staff users."""

    def has_permission(self, request, view) -> bool:
        """Check that the user is authenticated, active and marked as staff."""
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)
