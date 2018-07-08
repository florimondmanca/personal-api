"""Test the api_key app."""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.test import APITestCase, APIRequestFactory

from api_key.permissions import APIKeyPermission
from api_key.models import APIKey


class _TestView(APIView):

    permission_classes = [APIKeyPermission]

    def get(self, request):
        return Response()


test_view = _TestView.as_view()


class APIKeyTest(APITestCase):
    """Test the APIKey model."""

    def setUp(self):
        self.api_key = APIKey.objects.create(client_id='test')

    def test_key_generated_when_created(self):
        self.assertNotEqual(self.api_key.key, '')

    def test_key_long_enough(self):
        self.assertGreater(len(self.api_key.key), 16)


class APIKeyPermissionTest(APITestCase):
    """Test the API key permission class."""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_if_no_api_key_permission_denied(self):
        request = self.factory.get('/test/')
        response = test_view(request)
        self.assertEqual(response.status_code, 403)

    def test_if_invalid_api_key_provided_then_permission_denied(self):
        request = self.factory.get('/test/', HTTP_API_KEY='foo')
        response = test_view(request)
        self.assertEqual(response.status_code, 403)

    def test_if_valid_api_key_provided_then_permission_granted(self):
        api_key = APIKey.objects.create(client_id='test')
        request = self.factory.get('/test/', HTTP_API_KEY=api_key.key)
        response = test_view(request)
        self.assertEqual(response.status_code, 200)
