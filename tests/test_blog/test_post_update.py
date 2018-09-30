"""Test update of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory
from blog.models import Post


@authenticated
class PostUpdateTest(APITestCase):
    """Test the post update endpoint."""

    def setUp(self):
        self.post = PostFactory.create()

    def _get_default_payload(self):
        return {
            'title': 'Did everyone forget about apple juice?',
            'slug': 'did-everyone-forget-about-apple-juice',
            'content': 'Maybe.',
        }

    def _perform(self, **kwargs):
        payload = {
            **self._get_default_payload(),
            **kwargs,
        }
        url = f'/api/posts/{self.post.slug}/'
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        return response

    def test_update(self):
        payload = self._get_default_payload()
        self._perform(**payload)
        post = Post.objects.get(pk=self.post.pk)  # reload from DB
        for field, value in payload.items():
            self.assertEqual(value, getattr(post, field))

    def test_image_url_can_be_null(self):
        self._perform(image_url=None)

    def test_can_update_image_url(self):
        initial_url = 'https://fakeimg.pl/128/'
        new_url = 'https://fakeimg.pl/256/'

        post = PostFactory.create(image_url=initial_url)

        url = f'/api/posts/{post.slug}/'
        data = {'image_url': new_url}
        response = self.client.patch(url, data=data, format='json')

        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(pk=post.pk)  # reload from DB
        self.assertEqual(post.image_url, new_url)
