"""Blog views."""

from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .filters import PopularTagFilter, PostFilter
from .models import Post, Tag
from .pagination import PostPagination
from .serializers import PostDetailSerializer, PostSerializer, TagSerializer


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


class PopularTagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """API endpoints for popular tags."""

    queryset = (
        Tag.objects
        .with_post_counts(published_only=True)
        .filter(post_count__gt=0)  # Remove tags that have no published posts
        .order_by('-post_count', 'name')  # break count ties using name
    )
    serializer_class = TagSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_class = PopularTagFilter
