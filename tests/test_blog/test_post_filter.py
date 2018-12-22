"""Test list of blog posts."""

from datetime import timedelta
from time import sleep
from typing import List

from django.utils import timezone
from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory


@authenticated
class PostFilterListTest(APITestCase):
    """Test filtering the post list endpoint."""

    def perform(self, **params) -> List[dict]:
        response = self.client.get("/api/posts/", params)
        self.assertEqual(response.status_code, 200)
        return response.data["results"]

    def test_filter_by_slug(self):
        post = PostFactory.create(title="Hello, world!", slug="hello-world")
        posts = self.perform(slug=post.slug)
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["slug"], "hello-world")
        posts = self.perform(slug="good-bye")
        self.assertEqual(len(posts), 0)

    def test_filter_not_draft_returns_published_only(self):
        post = PostFactory.create()
        post.publish()
        posts = self.perform(draft=False)
        self.assertEqual(len(posts), 1)
        post_data = posts[0]
        self.assertEqual(post_data["id"], post.pk)
        self.assertFalse(post_data["is_draft"])

    def test_filter_not_draft_returns_in_published_date_order(self):
        now = timezone.now()
        yesterday = timezone.now() - timedelta(days=1)
        now_post = PostFactory.create(published=now)
        sleep(0.01)  # make `created` different for each post
        yesterday_post = PostFactory.create(published=yesterday)
        posts = self.perform(draft=False)
        by_published_desc = sorted(
            posts, key=lambda post: post["published"], reverse=True
        )
        self.assertListEqual(
            [p["id"] for p in by_published_desc], [now_post.pk, yesterday_post.pk]
        )

    def test_filter_draft_returns_drafts_only(self):
        # Create a draft
        PostFactory.create()
        # And a published post
        post = PostFactory.create()
        post.publish()

        posts = self.perform(draft=True)

        self.assertEqual(len(posts), 1)
        self.assertNotIn(post.pk, map(lambda post: post["id"], posts))
        for post in posts:
            self.assertTrue(post["is_draft"])
