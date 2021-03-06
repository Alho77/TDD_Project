from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AdminPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email='admin@test.com', password='admin1234')
        self.user = User.objects.create_user(
            email='test@test.com', password='test1234', name='User Test')
        self.client.force_login(self.admin_user)

    def test_user_listed(self):
        """Test if the user is listed in the user's page"""
        url = reverse('admin:app_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:app_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that user creation page works"""
        url = reverse('admin:app_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
