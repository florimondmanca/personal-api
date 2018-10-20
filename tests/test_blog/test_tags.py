"""Tests for the Tag model."""

from django.test import TestCase

from blog.models import Tag
from blog.factories import PostFactory


class TagManagerTest(TestCase):
    """Test the custom Tag model manager."""

    def test_with_post_counts_adds_post_count_to_queryset(self):
        Tag.objects.create(name='docker')
        PostFactory.create(tags=['python'])
        qs = Tag.objects.with_post_counts()
        values = qs.values('name', 'post_count')
        self.assertIn({'name': 'python', 'post_count': 1}, values)
        self.assertIn({'name': 'docker', 'post_count': 0}, values)
