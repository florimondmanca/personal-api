"""Test the site maps."""

from rest_framework.test import APITestCase
from rest_framework import status


class SitemapTest(APITestCase):
    """Test the site map."""

    def test_sitemap_exists(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
