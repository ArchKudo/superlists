from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTest(TestCase):

    def test_returns_None_if_no_token(self):
        # Create a new instance of PasswordlessAuthenticationBackend
        # and use the instance's authenticate method
        result = PasswordlessAuthenticationBackend().authenticate(
            uid='no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exist(self):
        email = "user@domain.com"
        token = Token.objects.create(email=email)
        created_user = PasswordlessAuthenticationBackend().authenticate(
            uid=token.uid)
        fetched_user = User.objects.get(email=email)
        self.assertEqual(created_user, fetched_user)

    def test_returns_existing_user_with_correct_email_if_token_exist(self):
        email = "user@domain.com"
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(uid=token.uid)
        self.assertEqual(user, existing_user)
