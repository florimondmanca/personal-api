"""Users factories."""

import factory
import factory.django

from .models import User


class UserFactory(factory.DjangoModelFactory):
    """Post object factory."""

    class Meta:  # noqa
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default creation behavior."""
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
