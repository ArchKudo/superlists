from django.test import TestCase
from unittest.mock import patch, call


@patch('accounts.views.auth')
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get('/accounts/login?token=xyzzyspoonshift1')
        self.assertRedirects(response, '/')

    def test_authenticate_uid_from_GET_request(self, mock_auth):
        self.client.get('/accounts/login?token=some_uid')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='some_uid'))

    def test_calls_auth_login_with_user(self, mock_auth):
        response = self.client.get('/accounts/login?token=some_uid')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request,
                 mock_auth.authenticate.return_value))

    def test_deny_login_if_user_unauthenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=some_uid')
        self.assertEqual(mock_auth.login.called, False)
