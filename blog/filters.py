"""Blog filters."""

import django_filters as filters
from .models import Post


class PostFilter(filters.FilterSet):
    """Filter for post objects."""

    draft = filters.BooleanFilter(
        field_name='published',
        lookup_expr='isnull',
    )
    tags__contain = filters.CharFilter(
        field_name='tags__contain',
        lookup_expr='contains',
    )

    class Meta:  # noqa
        model = Post
        fields = ('slug', 'tags__contain')
