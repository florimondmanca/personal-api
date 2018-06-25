"""Blog views."""

from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    """List of blog posts."""
    context_object_name = 'posts'
    model = Post
    # page_kwarg = 'page'
    # paginate_by =
    template_name = 'blog/post_list.html'
