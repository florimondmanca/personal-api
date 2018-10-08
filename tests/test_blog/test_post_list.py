"""Test list of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory, DraftFactory

_POST_FIELDS = {
    'id',
    'url',
    'slug',
    'title',
    'content',
    'image_url',
    'image_caption',
    'description',
    'created',
    'published',
    'is_draft',
    'tags',
}


@authenticated
class PostListTest(APITestCase):
    """Test the list endpoint for published posts."""

    def setUp(self):
        PostFactory.create_batch(3)
        DraftFactory.create()

    def perform(self, **params):
        response = self.client.get('/api/posts/', params)
        self.assertEqual(response.status_code, 200)
        return response

    def test_list(self):
        response = self.perform()
        self.assertEqual(len(response.data), 3)

    def test_returns_expected_fields(self):
        response = self.perform()
        expected = _POST_FIELDS
        self.assertSetEqual(expected, set(response.data[0]))

    def test_filter_by_slug(self):
        post = PostFactory.create(title='Hello, world!', slug='hello-world')
        response = self.perform(slug=post.slug)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['slug'], 'hello-world')

    def test_returns_published_only(self):
        response = self.perform()
        for post in response.data:
            self.assertFalse(post['is_draft'])
