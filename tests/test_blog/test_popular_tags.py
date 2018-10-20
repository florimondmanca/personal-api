"""Test the popular tags API."""


from typing import List

from rest_framework.test import APITestCase

from blog.factories import PostFactory
from tests.decorators import authenticated

_TAG_FIELDS = {
    'id',
    'name',
    'post_count',
}


@authenticated
class PopularTagTest(APITestCase):
    """Test the popular tags endpoint."""

    def setUp(self):
        PostFactory.create(tags=['python', 'docker'])
        PostFactory.create(tags=['python'])
        PostFactory.create()

    def perform(self, **params) -> List[dict]:
        response = self.client.get('/api/popular-tags/', params)
        self.assertEqual(response.status_code, 200)
        return response.data

    def test_list(self):
        tags = self.perform()
        self.assertEqual(len(tags), 2)

    def test_returns_expected_fields(self):
        tags = self.perform()
        expected = _TAG_FIELDS
        self.assertSetEqual(expected, set(tags[0]))

    def test_is_ordered_by_decreasing_post_count(self):
        tags = self.perform()
        sorted_by_post_count_desc = sorted(
            tags, key=lambda tag: tag['post_count'],
            reverse=True,
        )
        actual = [tag['name'] for tag in tags]
        expected = [tag['name']
                    for tag in sorted_by_post_count_desc]
        self.assertListEqual(actual, expected)
