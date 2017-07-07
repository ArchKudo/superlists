from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

    def test_validates_using_email_only(self):
        user = User(email='user@domain.com')
        user.full_clean()

    def test_email_is_primary_key(self):
        user = User(email='user@domain.com')
        self.assertEqual(user.pk, 'user@domain.com')
