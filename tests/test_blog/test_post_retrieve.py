"""Test retrieval of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory

from .test_post_list import _POST_FIELDS
_POST_DETAIL_FIELDS = _POST_FIELDS.union({'next', 'previous'})


@authenticated
class PostRetrieveTest(APITestCase):
    """Test the post retrieve endpoint."""

    def setUp(self):
        self.post = PostFactory.create()

    def perform(self, post=None):
        if post is None:
            post = self.post
        response = self.client.get(f'/api/posts/{post.slug}/')
        self.assertEqual(response.status_code, 200)
        return response

    def test_retrieve(self):
        self.perform()

    def test_returns_expected_fields(self):
        response = self.perform()
        expected = _POST_DETAIL_FIELDS
        self.assertSetEqual(expected, set(response.data))
