"""Blog views."""

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework.backends import DjangoFilterBackend

from .filters import PostFilter
from .models import Post, Tag
from .pagination import PostPagination
from .serializers import PostDetailSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """API endpoints for blog posts."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    filterset_class = PostFilter
    search_fields = ('title', 'description')
    pagination_class = PostPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer

    @action(methods=['patch'], detail=True)
    def publication(self, request, **kwargs):
        """Publish a blog post."""
        post = self.get_object()
        post.publish(request)
        serializer = self.get_serializer(instance=post)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def tags(self, request, **kwargs):
        """Return a list of tags with their number of posts."""
        tags = Tag.objects.with_post_counts().values('name', 'post_count')
        data = sorted(tags, key=lambda tag: tag['post_count'], reverse=True)
        return Response(data=data)
