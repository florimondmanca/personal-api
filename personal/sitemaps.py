"""Definition of site maps. They help search engines index the website.

Note: locations are defined as paths, not full URLs (no domain, not scheme).
See: https://docs.djangoproject.com/fr/2.1/ref/contrib/sitemaps
"""

from datetime import datetime
from typing import List

from django.contrib.sitemaps import Sitemap

from blog.models import Post


class PostSitemap(Sitemap):
    """Site map for blog posts."""

    # Frequency of change of each item.
    # Blog posts *may* be updated weekly.
    changefreq = 'weekly'

    def items(self):
        return Post.objects.published()

    def lastmod(self, obj: Post) -> datetime:
        return obj.modified


class TagSitemap(Sitemap):
    """Site map for blog tags."""

    # Tag pages *may* change monthly (in case of new posts).
    changefreq = 'monthly'

    def items(self) -> List[str]:
        """Return a list of all existing tags."""
        return list(Post.objects.distinct_tags())

    def location(self, tag: str) -> str:
        """Return the location of a tag."""
        return f'/t/{tag}'


class StaticSitemap(Sitemap):
    """Site map for static pages."""

    # Static pages *may* change weekly.
    changefreq = 'weekly'

    def items(self) -> List[str]:
        """Return a list of static pages paths."""
        return ['', 'about/me', 'about/tech']

    def location(self, page: str) -> str:
        """Return the location of a static page."""
        return f'/{page}'


sitemaps = {
    'posts': PostSitemap,
    'tags': TagSitemap,
    'static': StaticSitemap,
}
