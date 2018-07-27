"""Blog views."""

from io import StringIO

from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from banners.utils import Banner
from django_filters.rest_framework.backends import DjangoFilterBackend

from .filters import PostFilter
from .models import Post, Reaction
from .serializers import (PostDetailSerializer, PostSerializer,
                          ReactionSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """API endpoints for blog posts."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer

    @action(methods=['patch'], detail=True)
    def publication(self, request, **kwargs):
        """Publish a blog post."""
        post = self.get_object()
        post.publish()
        serializer = self.get_serializer(instance=post)
        return Response(serializer.data)


class ReactionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """API endpoints for blog post reactions."""

    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


def generate_banner(request, post: Post):
    """Generate and download a post banner."""
    image = Banner().generate(post.title)
    filename = f'{post.slug}.png'

    stream = StringIO()
    image.save(stream)

    response = HttpResponse()
    response['Content-Disposition'] = f'attachment; filename={filename}'
    response.write(stream.read())

    return response
