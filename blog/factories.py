"""Blog factories."""

import factory
import factory.django
from django.utils.timezone import now

from .models import Post


class BasePostFactory(factory.DjangoModelFactory):
    """Post object factory."""

    class Meta:  # noqa
        model = Post

    title = factory.Faker('sentence')
    content = factory.Faker('text')
    slug = factory.Faker('slug')


class PublishedPostFactory(BasePostFactory):
    """Factory of published blog posts."""

    published = factory.LazyAttribute(lambda o: now())


# Aliases
PostFactory = PublishedPostFactory
DraftFactory = BasePostFactory
