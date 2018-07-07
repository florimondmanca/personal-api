from django.db import models
from .utils import generate_key


class APIKey(models.Model):
    """Represents an API key."""

    created = models.DateTimeField(auto_now_add=True)
    client_id = models.CharField(max_length=50, unique=True)
    key = models.CharField(max_length=40, unique=True)

    class Meta:  # noqa
        ordering = ('-created',)
        verbose_name = 'API key'
        verbose_name_plural = 'API keys'

    def __str__(self):
        """Represent by the client ID."""
        return str(self.client_id)
