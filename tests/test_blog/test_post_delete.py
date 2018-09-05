"""Test deletion of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory


@authenticated
class PostDeleteTest(APITestCase):
    """Test the post update endpoint."""

    def setUp(self):
        self.post = PostFactory.create()

    def test_delete(self):
        url = f'/api/posts/{self.post.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
