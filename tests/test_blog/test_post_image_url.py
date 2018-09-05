"""Test computation of a blog post's image URL."""

import os
from contextlib import contextmanager

from django.core.files.images import ImageFile
from rest_framework.test import APITestCase
from tests.constants import TEST_ASSETS_DIR
from tests.decorators import authenticated

from blog.factories import PostFactory


@authenticated
class PostImageUrlTest(APITestCase):
    """Test the get_image_url() method."""

    @contextmanager
    def post_with_image(self, **kwargs):
        path = os.path.join(TEST_ASSETS_DIR, 'fake_image.png')
        with open(path, 'rb') as image_file:
            image = ImageFile(image_file)
            post = PostFactory.create(image=image, **kwargs)
        try:
            yield post
        finally:
            post.image.delete()

    def test_image_url_is_none_by_default(self):
        post = PostFactory.create()
        self.assertIsNone(post.get_image_url())

    def test_if_image_url_is_set_then_get_image_url_returns_it(self):
        url = 'https://fakeimg.pl/128/'
        post = PostFactory.create(image_url=url)
        self.assertEqual(url, post.get_image_url())

    def test_if_image_is_set_but_not_image_url_then_its_url_is_returned(self):
        with self.post_with_image() as post:
            url = post.get_image_url()
            self.assertIsNotNone(url)
            self.assertEqual(post.image.url, url)

    def test_image_url_is_absolute_when_doing_request(self):
        with self.post_with_image() as post:
            response = self.client.get(f'/api/posts/{post.slug}/')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.data['image_url'].startswith('http'))

    def test_if_image_and_image_url_are_set_then_image_is_used(self):
        with self.post_with_image(image_url='https://fakeimg.pl/128/') as post:
            url = post.get_image_url()
            self.assertEqual(post.image.url, url)
