from django.test import TestCase
from django.contrib.auth import get_user_model

from app import models

User = get_user_model()


def sample_user(email='test@test.com', password='1234'):
    """Create a sample user"""
    return User.objects.create_user(email=email, password=password)


class ModelsTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating user with email is successfull"""
        email = 'test@test.com'
        password = '1234'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_email_normalized(self):
        """Test the email for new user is normalized"""

        email = 'test@TEST.COM'
        password = '1234'
        user = User.objects.create_user(email, password)

        self.assertEqual(user.email, email.lower())

    def test_create_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            User.objects.create_user(None, '1234')

    def test_create_superuser(self):
        """Test creation superuser"""

        user = User.objects.create_superuser('test@test.com', 'su1234')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
