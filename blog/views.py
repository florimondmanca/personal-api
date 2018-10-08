"""Blog views."""

from collections import Counter

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework.backends import DjangoFilterBackend

from .filters import PostFilter
from .models import Post
from .serializers import PostDetailSerializer, PostSerializer
from .pagination import PostPagination


class PostViewSet(viewsets.ModelViewSet):
    """API endpoints for blog posts."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter
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
        # NOTE: Aggregation on Postgres ArrayField is hard without
        # leaving the ORM.
        # collections.Counter is super handy, so let's take all the tags
        # out of DB and do the count aggregation with it.
        # NOTE: Use generators for more efficient memory usage
        tags = Post.objects.with_tags().values_list('tag', flat=True)
        counter = Counter(tags)
        items = (
            {'tag': tag, 'post_count': counter[tag]}
            for tag in counter
        )
        data = sorted(items, key=lambda tag: tag['post_count'], reverse=True)
        return Response(data=data)
