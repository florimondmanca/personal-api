"""Blog views."""

from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from .forms import PostForm
from .models import Post


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
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('post-detail', pk=post.pk)
        return super().get(request, *args, **kwargs)


class PostEditView(TemplateView):
    """Create a new blog post."""

    template_name = 'blog/post_edit.html'

    def post(self, request, pk=None, **kwargs):
        """Update the blog post on POST."""
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=post.pk)
        return super().get(request, pk=pk, **kwargs)

    def get_context_data(self, **kwargs):
        """Insert post title and content in the context."""
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=context['pk'])
        context['title'] = post.title
        context['content'] = post.content
        return context
