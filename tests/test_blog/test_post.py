"""Blog tests."""

from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.models import Post
from blog.factories import PostFactory

_POST_FIELDS = {
    'id',
    'url',
    'slug',
    'title',
    'content',
    'created',
    'published',
    'is_draft',
}
_POST_DETAIL_FIELDS = _POST_FIELDS.union({'next', 'previous'})


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


@authenticated
class PostRetrieveTest(APITestCase):
    """Test the post retrieve endpoint."""

    def setUp(self):
        self.post = PostFactory.create()

    def perform(self, post=None):
        if post is None:
            post = self.post
        response = self.client.get(f'/api/posts/{post.slug}/')
        self.assertEqual(response.status_code, 200)
        return response

    def test_retrieve(self):
        self.perform()

    def test_returns_expected_fields(self):
        response = self.perform()
        expected = _POST_DETAIL_FIELDS
        self.assertSetEqual(expected, set(response.data))


class PostNavigationTestMixin:
    """Mixin for testing navigation fields on post detail."""

    relative_field: str

    def perform(self, post: Post):
        response = self.client.get(f'/api/posts/{post.slug}/')
        self.assertEqual(response.status_code, 200)
        return response

    def get_relative(self, published) -> Post:
        raise NotImplementedError

    def test_if_not_published_then_relative_is_none(self):
        response = self.perform(PostFactory.create())
        self.assertIsNone(response.data[self.relative_field])

    def test_if_published_but_no_relative_then_relative_is_none(self):
        post = PostFactory.create(published=timezone.now())
        response = self.perform(post)
        self.assertIsNone(response.data[self.relative_field])

    def test_if_published_and_has_relative_then_relative_with_fields(self):
        now = timezone.now()
        post = PostFactory.create(published=now)
        relative = self.get_relative(now)
        response = self.perform(post)
        expected = {
            'title': relative.title,
            'slug': relative.slug,
        }
        self.assertDictEqual(response.data[self.relative_field], expected)


@authenticated
class PostPreviousTest(PostNavigationTestMixin, APITestCase):
    """Test the previous field on retrieve endpoint."""

    relative_field = 'previous'

    def get_relative(self, published):
        later = published + timedelta(days=1)
        return PostFactory.create(published=later)


@authenticated
class PostNextTest(PostNavigationTestMixin, APITestCase):
    """Test the next field on retrieve endpoint."""

    relative_field = 'next'

    def get_relative(self, published):
        earlier = published - timedelta(days=1)
        return PostFactory.create(published=earlier)


@authenticated
class PostCreateTest(APITestCase):
    """Test the post create endpoint."""

    def setUp(self):
        self.post = PostFactory.build()

    def get_payload(self) -> dict:
        return {
            'title': self.post.title,
            'slug': self.post.slug,
            'content': self.post.content,
        }

    def perform(self, payload: dict = None, check_created=True):
        if payload is None:
            payload = self.get_payload()
        response = self.client.post(f'/api/posts/',
                                    data=payload, format='json')
        if check_created:
            self.assertEqual(response.status_code, 201)
        return response

    def test_create(self):
        self.perform()

    def test_missing_required_field_returns_bad_request(self):
        for field in 'title', 'slug':
            payload = self.get_payload()
            payload.pop(field)
            response = self.perform(payload=payload, check_created=False)
            self.assertEqual(response.status_code, 400)

    def test_returns_expected_fields(self):
        response = self.perform()
        expected = _POST_FIELDS
        self.assertSetEqual(expected, set(response.data))


@authenticated
class PostUpdateTest(APITestCase):
    """Test the post update endpoint."""

    def setUp(self):
        self.post = PostFactory.create()

    def test_update(self):
        payload = {
            'title': 'Did everyone forget about apple juice?',
            'slug': 'did-everyone-forget-about-apple-juice',
            'content': 'Maybe.',
        }
        url = f'/api/posts/{self.post.slug}/'
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, 200)


@authenticated
class PostPublishTest(APITestCase):
    """Test the endpoint to update published state of a post."""

    def setUp(self):
        self.post = PostFactory.create()

    def test_update_draft(self):
        self.assertTrue(self.post.is_draft)
        url = f'/api/posts/{self.post.slug}/publication/'
        response = self.client.patch(url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['is_draft'])


@authenticated
class PostDeleteTest(APITestCase):
    """Test the post update endpoint."""

    def setUp(self):
        self.post = PostFactory.create()

    def test_delete(self):
        url = f'/api/posts/{self.post.slug}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
