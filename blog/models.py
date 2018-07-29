"""Blog models."""

from contextlib import suppress
from typing import Union

from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator, slugify

from markdownx.models import MarkdownxField

from .utils import markdown_unformatted


class PostManager(models.Manager):
    """Custom object manager for blog posts."""

    def published(self):
        """Return published blog posts only."""
        return self.get_queryset().filter(published__isnull=False)


class Post(models.Model):
    """Represents a blog post."""

    objects = PostManager()

    SLUG_MAX_LENGTH = 80

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)
    content = MarkdownxField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
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

    @property
    def preview(self) -> str:
        """Return an unformatted preview of the post contents."""
        return Truncator(markdown_unformatted(self.content)).chars(200)

    def _find_published(self, **kwargs):
        """Filter and get the first published item in the queryset, or None."""
        if not self.published:
            return None
        qs = Post.objects.published().filter(**kwargs)
        return qs and qs[0] or None

    @property
    def previous(self) -> Union['Post', None]:
        """Return the previous published post.

        If the post is not published or there is no previous published post,
        returns None.
        """
        return self._find_published(published__lt=self.published)

    @property
    def next(self) -> Union['Post', None]:
        """Return the next published post.

        If the post is not published or there is no next published post,
        returns None.
        """
        return self._find_published(published__gt=self.published)

    def get_absolute_url(self) -> str:
        """Return the absolute URL of a blog post."""
        domain = Site.objects.get_current().domain
        return f'http://{domain}/{self.slug}'

    @classmethod
    def list_absolute_url(cls) -> str:
        """Return the absolute URL for the list of posts."""
        domain = Site.objects.get_current().domain
        return f'http://{domain}/'
