"""Testing decorators."""

from users.factories import UserFactory


def authenticated(cls):
    """Force login in the test case's setup."""

    class Decorated(cls):
        def setUp(self):
            super().setUp()
            self.client.force_login(UserFactory.create())

    return Decorated
