"""Blog views."""

from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """API endpoints for blog posts."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
