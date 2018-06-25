"""Blog models."""

import logging

from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField

logger = logging.getLogger('app.blog.models')


class Post(models.Model):
    """Represents a blog post."""

    SLUG_MAX_LENGTH = 50

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH)
    content = MarkdownxField(blank=True, default='')
    published = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Set slug when creating a post."""
        if not self.pk:
            self.slug = slugify(self.title)[:self.SLUG_MAX_LENGTH]

    def __str__(self) -> str:
        return str(self.title)

    class Meta:  # noqa
        ordering = ('-published',)
