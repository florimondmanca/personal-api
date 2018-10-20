"""Test blog post tags."""

from typing import List

from django.test import TestCase
from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.models import Post
from blog.factories import PostFactory


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


@authenticated
class TagListTest(TestCase):
    """Test the endpoint to retrieve the list of tags."""

    def setUp(self):
        PostFactory.create(tags=['python', 'webdev'])
        PostFactory.create(tags=['python', 'docker'])

    def perform(self):
        url = '/api/posts/tags/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return response.data

    def test_returns_list_of_tag_and_count(self):
        tags = self.perform()
        for tag in tags:
            self.assertIn('name', tag)
            self.assertIn('post_count', tag)

    def test_ordered_by_count(self):
        tags = self.perform()
        sorted_tags = sorted(
            tags,
            key=lambda tag: tag['post_count'],
            reverse=True,
        )
        self.assertListEqual(tags, sorted_tags)
