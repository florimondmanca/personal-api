"""Blog tests."""

from rest_framework.test import APITestCase

from blog.factories import PostFactory
from blog.models import Post

from .decorators import authenticated


_POST_FIELDS = {
    'id',
    'url',
    'slug',
    'title',
    'content',
    'published',
    'is_draft',
}


@authenticated
class PostListTest(APITestCase):
    """Test the post list endpoint."""

    def setUp(self):
        PostFactory.create_batch(3)

    def perform(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        return response

    def test_list(self):
        response = self.perform()
        self.assertEqual(len(response.data), 3)

    def test_returns_expected_fields(self):
        response = self.perform()
        expected = _POST_FIELDS
        self.assertSetEqual(expected, set(response.data[0]))


@authenticated
class PostRetrieveTest(APITestCase):
    """Test the post retrieve endpoint."""

    def setUp(self):
        self.post = PostFactory.create()

    def perform(self):
        response = self.client.get(f'/api/posts/{self.post.slug}/')
        self.assertEqual(response.status_code, 200)
        return response

    def test_retrieve(self):
        self.perform()

    def test_returns_expected_fields(self):
        response = self.perform()
        expected = _POST_FIELDS
        self.assertSetEqual(expected, set(response.data))


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
