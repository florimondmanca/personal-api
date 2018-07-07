"""Blog serializers."""

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for blog posts."""

    class Meta:  # noqa
        model = Post
        fields = ('id', 'url', 'title', 'slug', 'content', 'published')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'view_name': 'api:post-detail', 'lookup_field': 'slug'},
        }
