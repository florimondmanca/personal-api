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

    def published(self) -> models.QuerySet:
        """Return published blog posts only."""
        return self.get_queryset().filter(published__isnull=False)


class Post(models.Model):
    """Represents a blog post."""

    objects = PostManager()

    SLUG_MAX_LENGTH = 80

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=SLUG_MAX_LENGTH, unique=True)
    description = models.TextField(
        default="", blank=True, help_text="Used for social cards and RSS."
    )
    content = MarkdownxField(blank=True, default="")
    image_url = models.URLField(blank=True, null=True)
    image_caption = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)

    class Meta:  # noqa
        ordering = ("-published",)
        # NOTE: Django uses B-Tree indexes, enough for small datasets.
        indexes = [
            # `created` is used for ordering, which can be sped up by an index.
            models.Index(fields=["created"]),
            # `published` is filtered on a lot (to retrieve drafts)
            # and does not change very often.
            models.Index(fields=(["published"])),
        ]

    def save(self, *args, **kwargs):
        """Set slug when creating a post."""
        if not self.pk and not self.slug:
            self.slug = slugify(self.title)[: self.SLUG_MAX_LENGTH]
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Represent by its title."""
        return str(self.title)

    def publish(self, request=None):
        """Publish a blog post by setting its published date."""
        self.published = timezone.now()
        self.save()
        post_published.send(sender=Post, instance=self, request=request)

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
    def previous(self) -> Union["Post", None]:
        """Return the previous published post.

        If the post is not published or there is no previous published post,
        returns None.
        """
        return self._find_published("-published", published__lt=self.published)

    @property
    def next(self) -> Union["Post", None]:
        """Return the next published post.

        If the post is not published or there is no next published post,
        returns None.
        """
        return self._find_published("published", published__gt=self.published)

    def get_absolute_url(self) -> str:
        """Return the absolute URL path of a blog post."""
        return f"/{self.slug}/"

    @classmethod
    def list_absolute_url(cls) -> str:
        """Return the absolute URL path for the list of posts."""
        return "/"


class TagManager(models.Manager):
    """Custom manager for tag objects."""

    def with_post_counts(self, published_only: bool = False):
        """Add a `.post_count` attribute on each tag."""
        if published_only:
            published_filter = models.Q(posts__published__isnull=False)
        else:
            published_filter = None
        count_aggregate = models.Count("posts", filter=published_filter)
        return self.get_queryset().annotate(post_count=count_aggregate)


class Tag(models.Model):
    """Represents a group of posts related to similar content."""

    objects = TagManager()

    name = models.CharField(max_length=20)
    posts = models.ManyToManyField(to=Post, related_name="tags")

    def __str__(self) -> str:
        """Represent the tag by its name."""
        return str(self.name)
