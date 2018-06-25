"""Blog views."""

from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    """List of blog posts."""

    context_object_name = 'posts'
    model = Post
    template_name = 'blog/post_list.html'


class PostDetailView(DetailView):
    """Detail of a blog post."""

    context_object_name = 'post'
    model = Post
    slug_field = 'slug'
    template_name = 'blog/post_detail.html'
