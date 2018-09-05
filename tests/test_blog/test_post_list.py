"""Test list of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory

_POST_FIELDS = {
    'id',
    'url',
    'slug',
    'title',
    'content',
    'image_url',
    'description',
    'created',
    'published',
    'is_draft',
    'tags',
}


@authenticated
class PostListTest(APITestCase):
    """Test the post list endpoint."""

    def setUp(self):
        PostFactory.create_batch(3)

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

    def test_filter_not_draft_returns_published_only(self):
        post = PostFactory.create()
        post.publish()
        response = self.perform(draft=False)
        self.assertEqual(len(response.data), 1)
        post_data = response.data[0]
        self.assertEqual(post_data['id'], post.pk)
        self.assertFalse(post_data['is_draft'])

    def test_filter_draft_returns_drafts_only(self):
        post = PostFactory.create()
        post.publish()
        response = self.perform(draft=True)
        self.assertEqual(len(response.data), 3)
        self.assertNotIn(post.pk, map(lambda post: post['id'], response.data))
        for post in response.data:
            self.assertTrue(post['is_draft'])
