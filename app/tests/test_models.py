from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


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
