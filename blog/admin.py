"""Blog administration."""

from django.contrib import admin
from .models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin panel for blog posts."""

    list_display = ('__str__', 'created', 'modified', 'published',)
    list_filter = ('created', 'published',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin panel for tags."""
