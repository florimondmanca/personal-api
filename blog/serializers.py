"""Blog serializers."""

from typing import Union

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Post


class ImageUrlField(serializers.Field):
    """Custom field for a post's image URL."""

    def get_attribute(self, obj: Post) -> Post:
        """Pass the post object itself to `to_representation`."""
        return obj

    def to_representation(self, value: Post) -> str:
        """Return the absolute URL to the post's image."""
        relative_url = value.get_image_url()
        if relative_url is None:
            return None
        request = self.context.get('request')
        if not request:  # cannot build full URL without request
            return relative_url
        return request.build_absolute_uri(relative_url)

    def to_internal_value(self, data: str) -> str:
        """Return the incoming image URL itself."""
        return data


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for blog posts."""

    slug = serializers.SlugField(
        max_length=Post.SLUG_MAX_LENGTH,
        validators=[UniqueValidator(queryset=Post.objects.all())]
    )
    image_url = ImageUrlField(required=False)
    description = serializers.SerializerMethodField()

    def get_description(self, post: Post) -> str:
        """Return the post's description or its preview if not set."""
        return post.description if post.description else post.preview

    class Meta:  # noqa
        model = Post
        fields = ('id', 'url', 'title', 'slug', 'description', 'image_url',
                  'content', 'created', 'published', 'is_draft')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'view_name': 'api:post-detail', 'lookup_field': 'slug'},
        }


class MinimalPostSerializer(serializers.ModelSerializer):
    """Minimal serializer for post objects."""

    class Meta:  # noqa
        model = Post
        fields = ('title', 'slug',)


class PostDetailSerializer(PostSerializer):
    """Detail serializer for blog posts."""

    previous = MinimalPostSerializer(read_only=True)
    next = MinimalPostSerializer(read_only=True)

    class Meta(PostSerializer.Meta):  # noqa
        fields = PostSerializer.Meta.fields + ('previous', 'next',)
