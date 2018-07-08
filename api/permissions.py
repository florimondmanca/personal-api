from rest_framework import permissions

from api_key.permissions import APIKeyPermission


class APIKeyOrIsAuthenticated(permissions.BasePermission):
    """Authorize if valid API key or request is authenticated."""

    def has_permission(self, request, view):
        perms = [
            APIKeyPermission(),
            permissions.IsAuthenticated(),
        ]
        return any(perm.has_permission(request, view) for perm in perms)
