"""Test publication of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory


@authenticated
class PostPublishTest(APITestCase):
    """Test the endpoint to update published state of a post."""

    def setUp(self):
        self.post = PostFactory.create()

    def test_update_draft(self):
        self.assertTrue(self.post.is_draft)
        url = f"/api/posts/{self.post.slug}/publication/"
        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_draft"])
