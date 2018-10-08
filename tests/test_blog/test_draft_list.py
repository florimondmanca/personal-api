"""Test list of drafts."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import DraftFactory, PostFactory


@authenticated
class DraftListTest(APITestCase):
    """Test the endpoint to list drafts."""

    def setUp(self):
        DraftFactory.create_batch(3)
        PostFactory.create()

    def perform(self):
        url = '/api/drafts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return response

    def test_list(self):
        response = self.perform()
        self.assertEqual(len(response.data), 3)

    def test_returns_drafts_only(self):
        response = self.perform()
        for post in response.data:
            self.assertTrue(post['is_draft'])
