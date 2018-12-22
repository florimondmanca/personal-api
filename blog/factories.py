"""Blog factories."""

import factory
import factory.django

from .models import Post, Tag


class PostFactory(factory.DjangoModelFactory):
    """Post object factory."""

    class Meta:  # noqa
        model = Post

    title = factory.Faker("sentence")
    content = factory.Faker("text")
    slug = factory.Faker("slug")

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """Add the post to the given tags."""
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags was passed in
            for tag_name in extracted:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.tags.add(tag)
