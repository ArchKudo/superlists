from django.test import TestCase
from unittest.mock import patch
# import accounts.views


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
        self.assertEqual(subject, 'Your login link for to-do app')
        self.assertEqual(body, 'Use this link to login:')
        self.assertEqual(from_email, 'noreply@todoapp')
        self.assertEqual(to_list, ['user@domain.com'])

    def test_add_success_message(self):
        response = self.client.post(
            '/accounts/send_login_email',
            data={'email': 'user@domain.com'},
            follow=True)

        message = list(response.context['messages'])[0]

        self.assertEqual(message.message, 'Check email for login link...')
        self.assertEqual(message.tags, 'success')
