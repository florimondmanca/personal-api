from rest_framework import authentication

from .models import APIKey


class ApiKeyAuthentication(authentication.BaseAuthentication):
    """Authenticate via an API key."""

    def authenticate(self, request):
        api_key = request.META.get('HTTP_API_KEY', '')
        try:
            key = APIKey.objects.get(key=api_key)
            print(key)
        except APIKey.DoesNotExist:
            return None
        return (key.user, None)
