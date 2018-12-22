"""Blog filters."""

import django_filters as filters
from .models import Post, Tag


class PostFilter(filters.FilterSet):
    """Filter for post objects."""

    draft = filters.BooleanFilter(field_name="published", lookup_expr="isnull")
    tag = filters.CharFilter(field_name="tags", method="_filter_tags_contain")

    def _filter_tags_contain(self, queryset, name: str, value: str):
        return queryset.filter(tags__name=value)

    class Meta:  # noqa
        model = Post
        fields = ("draft", "slug", "tag")


class PopularTagFilter(filters.FilterSet):
    """Filter for popular tag objects."""

    limit = filters.NumberFilter(method="_limit")

    def _limit(self, queryset, name: str, value: int):
        """Limit to amount of elements in queryset."""
        return queryset[: int(value)]

    class Meta:  # noqa
        model = Tag
        fields = ("limit",)
