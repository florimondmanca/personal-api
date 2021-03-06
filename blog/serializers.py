"""Blog serializers."""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Post, Tag


class ImageUrlField(serializers.Field):
    """Custom field for a post's image URL."""

    def get_attribute(self, obj: Post) -> Post:
        """Pass the post object itself to `to_representation`."""
        return obj

    def to_representation(self, post: Post) -> str:
        """Return the absolute URL to the post's image."""
        relative_url = post.image_url
        if not relative_url:
            return None
        request = self.context.get("request")
        if not request:  # cannot build full URL without request
            return relative_url
        return request.build_absolute_uri(relative_url)

    def to_internal_value(self, data: str) -> str:
        """Return the incoming image URL itself."""
        return data


class DescriptionField(serializers.Field):
    """Custom field for post description."""

    def get_attribute(self, obj: Post) -> Post:
        """Pass the post object itself to `to_representation`."""
        return obj

    def to_representation(self, post: Post) -> str:
        return post.description if post.description else post.preview

    def to_internal_value(self, data: str) -> str:
        return data


class TagField(serializers.RelatedField):
    """Custom related field for post tags."""

    queryset = Tag.objects.all()

    def to_representation(self, tag: Tag) -> str:
        """Output tag as its string representation."""
        return str(tag)

    def to_internal_value(self, data: str) -> Tag:
        """Ingest tag by getting/creating it from the given tag name."""
        tag, created = Tag.objects.get_or_create(name=data)
        return tag


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for blog posts."""

    slug = serializers.SlugField(
        max_length=Post.SLUG_MAX_LENGTH,
        validators=[UniqueValidator(queryset=Post.objects.all())],
    )
    tags = TagField(many=True, required=False)
    image_url = ImageUrlField(required=False, allow_null=True)
    description = DescriptionField(required=False)

    class Meta:  # noqa
        model = Post
        fields = (
            "id",
            "url",
            "title",
            "slug",
            "description",
            "image_url",
            "image_caption",
            "content",
            "created",
            "published",
            "is_draft",
            "tags",
        )
        lookup_field = "slug"
        extra_kwargs = {
            "url": {"view_name": "api:post-detail", "lookup_field": "slug"},
            "published": {"read_only": True},
        }


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    post_count = serializers.IntegerField()  # field is an annotation

    class Meta:  # noqa
        model = Tag
        fields = ("id", "name", "post_count")


class MinimalPostSerializer(serializers.ModelSerializer):
    """Minimal serializer for post objects."""

    class Meta:  # noqa
        model = Post
        fields = ("title", "slug", "tags")


class PostDetailSerializer(PostSerializer):
    """Detail serializer for blog posts."""

    previous = MinimalPostSerializer(read_only=True)
    next = MinimalPostSerializer(read_only=True)

    class Meta(PostSerializer.Meta):  # noqa
        fields = PostSerializer.Meta.fields + ("previous", "next")
