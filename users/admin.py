"""Users administration."""

from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from .models import User


@register(User)
class MyUserAdmin(UserAdmin):
    """User admin panel."""
