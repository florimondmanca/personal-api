"""Test blog post tags."""

from django.test import TestCase
from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.models import Post
from blog.factories import PostFactory, DraftFactory


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

    def test_if_post_is_draft_then_not_included(self):
        DraftFactory.create(tags=['python'])
        response = self.perform()
        self.assertEqual(len(response.data), 0)


class DistinctTagsTest(TestCase):
    """Test the Post manager's method to retrieve distinct tags."""

    def setUp(self):
        PostFactory.create(tags=['python', 'webdev'])
        PostFactory.create(tags=['python', 'docker'])
        PostFactory.create(tags=[])

    def test_distinct_tags_returns_all_distinct_tags(self):
        tags = list(Post.objects.distinct_tags())
        self.assertEqual(len(tags), 3, tags)
        self.assertSetEqual(set(tags), {'docker', 'python', 'webdev'})


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
            self.assertIn('tag', tag)
            self.assertIn('post_count', tag)

    def test_ordered_by_count(self):
        tags = self.perform()
        sorted_tags = sorted(
            tags,
            key=lambda tag: tag['post_count'],
            reverse=True,
        )
        self.assertListEqual(tags, sorted_tags)
