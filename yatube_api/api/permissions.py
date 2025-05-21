from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение, позволяющее только автору изменять объект."""

    def has_object_permission(self, request, view, obj):
        """Проверка прав доступа."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
