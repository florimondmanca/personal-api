"""Blog views."""

from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import PostCreateForm


class PostListView(TemplateView):
    """List of blog posts."""

    template_name = 'blog/post_list.html'


class PostDetailView(TemplateView):
    """Detail of a blog post."""

    template_name = 'blog/post_detail.html'


class PostCreateView(TemplateView):
    """Create a new blog post."""

    template_name = 'blog/post_create.html'

    def post(self, request, *args, **kwargs):
        """Create the blog post on POST."""
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return super().get(request, *args, **kwargs)
