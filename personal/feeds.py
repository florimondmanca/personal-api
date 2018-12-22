"""Syndication feeds."""
from django.contrib.syndication.views import Feed
from django.utils import timezone

from blog.models import Post


class LatestPostsFeed(Feed):
    """RSS feed for the latest blog posts."""

    LIMIT_ITEMS = 5

    title = "CodeSail by Florimond Manca"
    description = "Updates on latest blog posts published on CodeSail"
    author_name = "Florimond Manca"
    categories = ("Blogging", "Technology", "Web development", "Software Engineering")
    ttl = 600  # time to live, minutes

    def link(self) -> str:
        return Post.list_absolute_url()

    def items(self):
        return Post.objects.published()[: self.LIMIT_ITEMS]

    def item_title(self, post: Post) -> str:
        return post.title

    def item_description(self, post: Post) -> str:
        return post.description or post.preview

    def item_pubdate(self, post: Post) -> str:
        return post.published

    def feed_copyright(self) -> str:
        year = timezone.now().year
        return f"Copyright © {year}, Florimond Manca"
