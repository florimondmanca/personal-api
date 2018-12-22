"""Test creation of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory
from .test_post_list import _POST_FIELDS


@authenticated
class PostCreateTest(APITestCase):
    """Test the post create endpoint."""

    def setUp(self):
        self.post = PostFactory.build()

    def get_payload(self) -> dict:
        return {
            "title": self.post.title,
            "slug": self.post.slug,
            "content": self.post.content,
        }

    def perform(self, payload: dict = None, check_created=True):
        if payload is None:
            payload = self.get_payload()
        response = self.client.post(f"/api/posts/", data=payload, format="json")
        if check_created:
            self.assertEqual(response.status_code, 201)
        return response

    def test_create(self):
        self.perform()

    def test_missing_required_field_returns_bad_request(self):
        for field in "title", "slug":
            payload = self.get_payload()
            payload.pop(field)
            response = self.perform(payload=payload, check_created=False)
            self.assertEqual(response.status_code, 400)

    def test_returns_expected_fields(self):
        response = self.perform()
        expected = _POST_FIELDS
        self.assertSetEqual(expected, set(response.data))
