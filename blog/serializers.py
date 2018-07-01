"""Blog serializers."""

from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for blog posts."""

    class Meta:  # noqa
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'published')
