"""Blog signals."""

from django.contrib.sitemaps import ping_google
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import Signal, receiver

post_published = Signal(providing_args=['instance', 'request'])


@receiver(post_published)
def ping_google_on_publish_post(sender, instance, request=None, **kwargs):
    """Let Google know that sitemap was updated when a post is published."""
    def _skip(reason: str):
        print('Skipped ping_google because', reason)

    if request is None:
        _skip('no request was given')
        return

    site = get_current_site(request)

    if 'localhost' in site.domain:
        _skip('running on localhost')
        return

    if site.domain == 'example.com':
        _skip('most definitely testing')
        return

    ping_google()
    print('Pinged Google about updated sitemap')
