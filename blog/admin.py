"""Blog administration."""

from django.contrib import admin
from .models import Post, Reaction

from banners.views import download_banner


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin panel for blog posts."""

    list_display = ('__str__', 'created', 'published',)
    list_filter = ('created', 'published',)

    actions = ['generate_banner']

    def generate_banner(self, request, queryset):
        post = queryset.first()
        filename = f'{post.slug}.png'
        return download_banner(request, text=post.title, filename=filename)

    generate_banner.short_description = (
        'Generate banner for first selected post'
    )


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    """Admin panel for reactions."""

    list_display = ('created', 'post',)
    list_filter = ('created',)
