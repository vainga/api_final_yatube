"""Модуль для проверки полномочий действий пользователя над объектами."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Проверяет полномочие на изменение или удаление поста только его автором.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
