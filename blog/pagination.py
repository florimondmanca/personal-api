"""Blog pagination classes."""

from rest_framework.pagination import CursorPagination


class PostPagination(CursorPagination):
    """Pagination configuration for blog posts."""

    page_size = 10  # Must be set, non-configurable by client
    ordering = '-published'  # The default
