"""Test searching the list of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory


@authenticated
class PostSearchListTest(APITestCase):
    """Test searching on the post list endpoint."""

    def setUp(self):
        self.post1 = PostFactory.create(title='Getting Started With Python')
        self.post2 = PostFactory.create(title='Test', slug='foo')
        self.post3 = PostFactory.create(tags=['docker'])

    def search(self, term: str):
        url = '/api/posts/'
        response = self.client.get(url, {'search': term})
        self.assertEqual(response.status_code, 200)
        return response.data['results']

    def test_returns_posts_matching_title(self):
        results = self.search('Python')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.post1.pk)

    def test_returns_posts_matching_slug(self):
        results = self.search('foo')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.post2.pk)

    def test_does_not_return_posts_matching_tags(self):
        results = self.search('docker')
        self.assertEqual(len(results), 0)
