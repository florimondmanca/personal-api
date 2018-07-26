"""Blog administration."""

from django.contrib import admin
from .models import Post, Reaction


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin panel for blog posts."""

    list_display = ('__str__', 'created', 'published',)
    list_filter = ('created', 'published',)


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    """Admin panel for reactions."""

    list_display = ('created', 'post',)
    list_filter = ('created',)
