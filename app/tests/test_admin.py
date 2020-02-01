from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AdminPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email='admin@test.com', password='admin1234')
        # TODO: check why need username (Err: UNIQUE constraint failed: app_user.username)
        self.user = User.objects.create_user(
            email='test@test.com', password='test1234', name='User Test', username='test')
        self.client.force_login(self.admin_user)

    def test_user_listed(self):
        """Test if the user is listed in the user's page"""
        url = reverse('admin:app_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)
