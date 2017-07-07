from accounts.models import Token
from django.test import TestCase


class TokenModelTest(TestCase):

    def test_associates_uid_with_email(self):
        token_one = Token.objects.create(email='user@domain.com')
        token_two = Token.objects.create(email='user@domain.com')
        self.assertNotEqual(token_one.uid, token_two.uid)
