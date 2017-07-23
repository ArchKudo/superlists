from django.test import TestCase
from django.contrib import auth

User = auth.get_user_model()


class UserModelTest(TestCase):

    def test_validates_using_email_only(self):
        user = User(email='user@domain.com')
        user.full_clean()

    def test_email_is_primary_key(self):
        user = User(email='user@domain.com')
        self.assertEqual(user.pk, 'user@domain.com')

    def test_auth_login(self):
        user = User.objects.create(email='user@domain.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)
