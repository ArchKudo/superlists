from accounts.authentication import PasswordlessAuthenticationBackend
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        User.objects.create(email='other_user@domain.com')
        desired_user = User.objects.create(email='user@domain.com')
        found_user = PasswordlessAuthenticationBackend().get_user(
            'user@domain.com')
        self.assertEqual(found_user, desired_user)

    def test_return_None_if_no_user_with_given_email(self):
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user(
                'user@domain.com'))
