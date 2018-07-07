from rest_framework import permissions

from .models import APIKey


class HasAPIAccess(permissions.BasePermission):
    """Authorize a request based on its HTTP_API_KEY header."""

    message = 'Invalid or missing API key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        return APIKey.objects.filter(key=api_key).exists()
