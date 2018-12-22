"""Test list of blog posts."""

from typing import List

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory

_POST_FIELDS = {
    "id",
    "url",
    "slug",
    "title",
    "content",
    "image_url",
    "image_caption",
    "description",
    "created",
    "published",
    "is_draft",
    "tags",
}


@authenticated
class PostListTest(APITestCase):
    """Test the post list endpoint."""

    def setUp(self):
        PostFactory.create_batch(3)

    def perform(self, **params) -> List[dict]:
        response = self.client.get("/api/posts/", params)
        self.assertEqual(response.status_code, 200)
        return response.data["results"]

    def test_list(self):
        posts = self.perform()
        self.assertEqual(len(posts), 3)

    def test_returns_expected_fields(self):
        posts = self.perform()
        expected = _POST_FIELDS
        self.assertSetEqual(expected, set(posts[0]))
