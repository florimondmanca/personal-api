"""Blog factories."""

import factory
import factory.django

from .models import Post


class PostFactory(factory.DjangoModelFactory):
    """Post object factory."""

    class Meta:  # noqa
        model = Post

    title = factory.Faker('sentence')
    content = factory.Faker('text')
    slug = factory.Faker('slug')
