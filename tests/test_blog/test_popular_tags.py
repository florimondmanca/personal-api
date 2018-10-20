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
        posts = [
            PostFactory.create(tags=['python', 'docker']),
            PostFactory.create(tags=['python']),
            PostFactory.create(tags=['aws']),
            PostFactory.create(),
        ]
        for post in posts:
            post.publish()

    def perform(self, **params) -> List[dict]:
        response = self.client.get('/api/popular-tags/', params)
        self.assertEqual(response.status_code, 200)
        return response.data

    def test_list(self):
        tags = self.perform()
        self.assertEqual(len(tags), 3)

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

    def test_limit_query_parameter_limits_amount_of_returned_values(self):
        tags = self.perform(limit=1)
        self.assertEqual(len(tags), 1)
        with_most_posts = 'python'
        self.assertEqual(tags[0]['name'], with_most_posts)

    def test_does_not_include_drafts(self):
        PostFactory.create(tags=['angular'])  # not published
        tags = self.perform()
        self.assertNotIn('angular', map(lambda tag: tag['name'], tags))

    def test_equal_count_tags_sorted_in_alphabetical_order(self):
        tags = self.perform()
        self.assertEqual('aws', tags[1]['name'])
        self.assertEqual('docker', tags[2]['name'])
