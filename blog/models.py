"""Blog models."""

from typing import Union

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator, slugify

from markdownx.models import MarkdownxField

from .dbfunctions import Unnest
from .signals import post_published
from .utils import markdown_unformatted


class PostManager(models.Manager):
    """Custom object manager for blog posts."""

    def published(self):
        """Return published blog posts only."""
        return self.get_queryset().filter(published__isnull=False)

    def distinct_tags(self):
        """Return the list of distinct blog post tags.

        Inspired by
        -----------
        https://dba.stackexchange.com/questions/126412/array-integer-how-to-get-all-distinct-values-in-a-table-and-count-them
        """
        queryset = self.get_queryset()
        unnest_tags = Unnest('tags', distinct=True)
        with_distinct_tags = queryset.annotate(tag=unnest_tags)
        return with_distinct_tags.values_list('tag', flat=True).distinct()


class Post(models.Model):
    """Represents a blog post."""

    objects = PostManager()

    SLUG_MAX_LENGTH = 80

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)
    description = models.TextField(
        default='', blank=True,
        help_text='Used for social cards and RSS.')
    content = MarkdownxField(blank=True, default='')
    image_url = models.URLField(blank=True, null=True)
    image_caption = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)
    tags = ArrayField(
        models.CharField(max_length=100), blank=True, default=list)

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
        post_published.send(sender=Post, instance=self)

    @property
    def is_draft(self) -> bool:
        """Return whether the post is a draft."""
        return self.published is None

    @property
    def preview(self) -> str:
        """Return an unformatted preview of the post contents."""
        return Truncator(markdown_unformatted(self.content)).chars(200)

    def _find_published(self, order_by, **kwargs):
        """Filter and get the first published item in the queryset, or None."""
        if not self.published:
            return None
        qs = Post.objects.published().order_by(order_by).filter(**kwargs)
        return qs and qs[0] or None

    @property
    def previous(self) -> Union['Post', None]:
        """Return the previous published post.

        If the post is not published or there is no previous published post,
        returns None.
        """
        return self._find_published('-published', published__lt=self.published)

    @property
    def next(self) -> Union['Post', None]:
        """Return the next published post.

        If the post is not published or there is no next published post,
        returns None.
        """
        return self._find_published('published', published__gt=self.published)

    def get_absolute_url(self) -> str:
        """Return the absolute URL path of a blog post."""
        return f'/{self.slug}/'

    @classmethod
    def list_absolute_url(cls) -> str:
        """Return the absolute URL path for the list of posts."""
        return '/'
