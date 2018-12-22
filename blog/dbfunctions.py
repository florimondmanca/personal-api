"""Database functions."""

from django.db.models import Func


class Unnest(Func):
    """The PostgreSQL UNNEST function."""

    function = "UNNEST"
