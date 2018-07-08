"""Blog views."""

from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """API endpoints for blog posts."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('slug',)
