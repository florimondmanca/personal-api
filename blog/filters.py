"""Blog filters."""

import django_filters as filters
from .models import Post


class PostFilter(filters.FilterSet):
    """Filter for post objects."""

    draft = filters.BooleanFilter(
        field_name='published',
        lookup_expr='isnull',
    )
    tag = filters.CharFilter(
        field_name='tags',
        method='_filter_tags_contain'
    )

    def _filter_tags_contain(self, queryset, name: str, value: str):
        return queryset.filter(tags__contains=[value])

    class Meta:  # noqa
        model = Post
        fields = ('slug', 'tag')
