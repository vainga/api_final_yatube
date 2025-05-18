from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Определеет права доступа к ресурсам."""
    def has_permission(self, request, view):
        """Проверка пользователя на доступ к ресурсам"""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Проверка пользователя на доступ к ресурсам объекта"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
