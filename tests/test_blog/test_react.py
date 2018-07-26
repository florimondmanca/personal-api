"""Post reactions tests."""

from rest_framework.test import APITestCase
from tests.decorators import authenticated

from blog.factories import PostFactory


@authenticated
class CreateReactionTest(APITestCase):
    """Test the reaction create endpoint."""

    def setUp(self):
        self.post = PostFactory.create()

    def test_create_reaction_increases_post_reaction_count_by_one(self):
        initial = self.post.reaction_count
        data = {'post': self.post.pk}
        response = self.client.post('/api/reactions/', data=data)
        self.assertEqual(response.status_code, 201)
        final = self.post.reaction_count
        self.assertEqual(final, initial + 1)
