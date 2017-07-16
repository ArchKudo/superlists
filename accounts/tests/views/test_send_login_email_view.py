from accounts.models import Token
from django.test import TestCase
from unittest.mock import patch, call


class SendLoginEmailViewTest(TestCase):

    def test_redirect_to_home_page(self):
        response = self.client.post(
            '/accounts/send_login_email', data={'email': 'user@domain.com'})
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_send_email_using_POST(self, mock_send_mail):

        self.client.post('/accounts/send_login_email',
                         data={'email': 'user@domain.com'})

        self.assertTrue(mock_send_mail.called, True)

        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for To-do app MVC')
        self.assertIn('Use this link to login:', body)
        self.assertEqual(from_email, 'noreply@todoapp')
        self.assertEqual(to_list, ['user@domain.com'])

    @patch('accounts.views.messages')
    def test_add_success_message(self, mock_messages):
        response = self.client.post(
            '/accounts/send_login_email',
            data={'email': 'user@domain.com'},)

        expected = 'Check your email for login link'

        self.assertEqual(mock_messages.success.call_args,
                         call(response.wsgi_request, expected))

    def test_creates_token_associated_with_email(self):
        self.client.post('/accounts/send_login_email',
                         data={'email': 'user@domain.com'})
        token = Token.objects.first()

        self.assertEqual(token.email, 'user@domain.com')

    @patch('accounts.views.send_mail')
    def test_send_links_to_login_using_token_id(self, mock_mail):
        self.client.post('/accounts/send_login_email',
                         data={'email': 'user@domain.com'})

        token = Token.objects.first()
        print(type(token))
        expected_url = f'http://testserver/accounts/login?token={token.uid}'

        (subject, body, from_email, to_list), kwargs = mock_mail.call_args

        self.assertIn(expected_url, body)
