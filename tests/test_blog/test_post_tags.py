"""Test blog post tags."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory


@authenticated
class SearchByTagTest(APITestCase):
    """Test the filtering of the blog post list for a given tag."""

    def perform(self):
        url = '/api/posts/'
        response = self.client.get(url, data={'tag': 'python'})
        self.assertEqual(response.status_code, 200)
        return response

    def test_if_post_has_tag_then_included(self):
        PostFactory.create(tags=['python', 'webdev'])
        response = self.perform()
        self.assertEqual(len(response.data), 1)

    def test_if_post_does_not_have_tag_then_not_included(self):
        PostFactory.create(tags=['javascript', 'webdev'])
        response = self.perform()
        self.assertEqual(len(response.data), 0)
