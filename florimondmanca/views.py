"""Project views."""

from django.views.generic import RedirectView


class IndexView(RedirectView):
    """Home page."""

    pattern_name = 'post-list'
