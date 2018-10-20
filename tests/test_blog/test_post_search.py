"""Test searching the list of blog posts."""

from typing import List

from rest_framework.test import APITestCase

from blog.factories import PostFactory
from tests.decorators import authenticated


@authenticated
class PostSearchListTest(APITestCase):
    """Test searching on the post list endpoint."""

    def setUp(self):
        self.post1 = PostFactory.create(title='Getting Started With Python')
        self.post2 = PostFactory.create(description='Ruby: From Zero To Hero')
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

    def test_returns_posts_matching_description(self):
        results = self.search('Ruby')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.post2.pk)

    def test_does_not_return_posts_matching_tags(self):
        results = self.search('docker')
        self.assertEqual(len(results), 0)


@authenticated
class SearchByTagTest(APITestCase):
    """Test the filtering of the blog post list for a given tag."""

    def perform(self) -> List[dict]:
        url = '/api/posts/'
        response = self.client.get(url, data={'tag': 'python'})
        self.assertEqual(response.status_code, 200)
        return response.data['results']

    def test_if_post_has_tag_then_included(self):
        PostFactory.create(tags=['python', 'webdev'])
        posts = self.perform()
        self.assertEqual(len(posts), 1)

    def test_if_post_does_not_have_tag_then_not_included(self):
        PostFactory.create(tags=['javascript', 'webdev'])
        posts = self.perform()
        self.assertEqual(len(posts), 0)
