"""Blog administration."""

from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin panel for blog posts."""

    list_display = ('__str__', 'published',)
    list_filter = ('published',)
    readonly_fields = ('slug',)