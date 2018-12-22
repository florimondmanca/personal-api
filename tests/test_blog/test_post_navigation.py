"""Test navigation between blog posts."""

from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory
from blog.models import Post


class PostNavigationTestMixin:
    """Mixin for testing navigation fields on post detail."""

    relative_field: str

    def perform(self, post: Post):
        response = self.client.get(f"/api/posts/{post.slug}/")
        self.assertEqual(response.status_code, 200)
        return response

    def get_relative(self, published) -> Post:
        raise NotImplementedError

    def test_if_not_published_then_relative_is_none(self):
        response = self.perform(PostFactory.create())
        self.assertIsNone(response.data[self.relative_field])

    def test_if_published_but_no_relative_then_relative_is_none(self):
        post = PostFactory.create(published=timezone.now())
        response = self.perform(post)
        self.assertIsNone(response.data[self.relative_field])

    def test_if_published_and_has_relative_then_relative_with_fields(self):
        now = timezone.now()
        post = PostFactory.create(published=now)
        relative = self.get_relative(now)
        response = self.perform(post)
        expected = {"title": relative.title, "slug": relative.slug}
        data = response.data[self.relative_field]
        actual = {field: data.get(field) for field in expected}
        self.assertEqual(actual, expected)


@authenticated
class PostPreviousTest(PostNavigationTestMixin, APITestCase):
    """Test the previous field on retrieve endpoint."""

    relative_field = "previous"

    def get_relative(self, published):
        earlier = published - timedelta(days=1)
        return PostFactory.create(published=earlier)


@authenticated
class PostNextTest(PostNavigationTestMixin, APITestCase):
    """Test the next field on retrieve endpoint."""

    relative_field = "next"

    def get_relative(self, published):
        later = published + timedelta(days=1)
        return PostFactory.create(published=later)
