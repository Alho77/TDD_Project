from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from app.models import Tag
from recipe.serializers import TagSerializer

TAG_URL = reverse('recipe:tag-list')
USER = get_user_model()


class PublicTagApiTest(TestCase):
    """Test the publicly available tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_retrive_tag_unauthorized(self):
        """Test retriving tag require authentication"""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    """Test authenticated user tags api"""

    def setUp(self):
        self.user = USER.objects.create_user('test@test.com', '1234')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_for_user(self):
        """Test that tags are retrived only for authenticated user"""
        user2 = USER.objects.create_user('other@test.com', '1234')

        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(len(res.data), 1)

    def test_create_tag_successfully(self):
        """Test creating new tag"""
        payload = {'name': 'Fruit'}
        res = self.client.post(TAG_URL, payload)

        exists = Tag.objects.filter(user=self.user, name=payload['name'])

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating tag with invalid data"""
        payload = {'name': ''}
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
