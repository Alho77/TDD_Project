from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


USER = get_user_model()
CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return USER.objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating user with valid payload"""
        payload = {
            'email': 'test@test.com',
            'password': '1234',
            'name': 'Test User'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = USER.objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'test@test.com',
            'password': '1234',
            'name': 'Test User'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 4 characters"""
        payload = {'email': 'test@test.com', 'password': '123'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = USER.objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)