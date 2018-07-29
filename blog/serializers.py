"""Blog serializers."""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for blog posts."""

    slug = serializers.SlugField(
        max_length=Post.SLUG_MAX_LENGTH,
        validators=[UniqueValidator(queryset=Post.objects.all())]
    )

    class Meta:  # noqa
        model = Post
        fields = ('id', 'url', 'title', 'slug', 'content',
                  'created', 'published', 'is_draft')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'view_name': 'api:post-detail', 'lookup_field': 'slug'},
        }


class PostDetailSerializer(PostSerializer):
    """Detail serializer for blog posts."""

    previous = serializers.CharField(source='previous.slug', default=None)
    next = serializers.CharField(source='next.slug', default=None)

    class Meta(PostSerializer.Meta):  # noqa
        fields = PostSerializer.Meta.fields + ('previous', 'next',)
