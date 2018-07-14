"""Blog views."""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

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

    @action(methods=['patch'], detail=True)
    def publication(self, request, **kwargs):
        """Publish a blog post."""
        post = self.get_object()
        post.publish()
        serializer = self.get_serializer(instance=post)
        return Response(serializer.data)
