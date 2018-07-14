"""Blog filters."""

import django_filters as filters
from .models import Post


class PostFilter(filters.FilterSet):
    """Filter for post objects."""

    draft = filters.BooleanFilter(
        field_name='published', method='_filter_is_draft')

    class Meta:  # noqa
        model = Post
        fields = ('slug',)

    def _filter_is_draft(self, qs, name, value):
        isnull = bool(value)
        lookup_expr = f'{name}__isnull'
        return qs.filter(**{lookup_expr: isnull})
