from rest_framework import permissions

from .models import APIKey


class APIKeyPermission(permissions.BasePermission):
    """Authorize via an API key."""

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        print(api_key)
        return APIKey.objects.filter(key=api_key).exists()
