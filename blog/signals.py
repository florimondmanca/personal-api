"""Blog signals."""

from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.dispatch import Signal, receiver

post_published = Signal(providing_args=['instance'])


@receiver(post_published)
def ping_google_on_publish_post(sender, instance, **kwargs):
    """Let Google know that sitemap was updated when a post is published."""
    if settings.TESTING:
        print('Skipped ping_google() because this was a test')
    else:
        ping_google()
