from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает анонимному пользователю только безопасные запросы.

    Предоставляет права на осуществление запросов
    только суперпользователю или админу.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminModeratOrAuthorOrReadOnly(permissions.BasePermission):
    """Проверка авторизации и доступа к объектам."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or (obj.author == request.user))


class IsAdmin(permissions.BasePermission):
    """Предоставляет права только суперпользователю или админу."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
