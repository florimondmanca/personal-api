"""Blog views."""

from django.views.generic import TemplateView


class PostListView(TemplateView):
    """List of blog posts."""

    template_name = 'blog/post_list.html'


class PostDetailView(TemplateView):
    """Detail of a blog post."""

    template_name = 'blog/post_detail.html'
