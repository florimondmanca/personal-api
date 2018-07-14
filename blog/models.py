"""Blog models."""

import logging

from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from markdownx.models import MarkdownxField

logger = logging.getLogger('app.blog.models')


class Post(models.Model):
    """Represents a blog post."""

    SLUG_MAX_LENGTH = 80

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)
    content = MarkdownxField(blank=True, default='')
    published = models.DateTimeField(blank=True, null=True)

    class Meta:  # noqa
        ordering = ('-published',)

    def save(self, *args, **kwargs):
        """Set slug when creating a post."""
        if not self.pk:
            self.slug = slugify(self.title)[:self.SLUG_MAX_LENGTH]
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Represent by its title."""
        return str(self.title)

    def publish(self):
        """Publish a blog post by setting its published date."""
        self.published = timezone.now()
        self.save()

    @property
    def is_draft(self) -> bool:
        """Return whether the post is a draft."""
        return self.published is None
