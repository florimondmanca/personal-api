"""Test publication of blog posts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import DraftFactory


@authenticated
class DraftPublishTest(APITestCase):
    """Test the endpoint to publish draft blog posts."""

    def setUp(self):
        self.post = DraftFactory.create()

    def test_publish_draft(self):
        self.assertTrue(self.post.is_draft)
        url = f'/api/drafts/{self.post.slug}/publication/'
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['is_draft'])
