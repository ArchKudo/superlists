from django.test import TestCase
import accounts.views


class SendLoginEmailViewTest(TestCase):

    def test_redirect_to_home_page(self):
        response = self.client.post(
            '/accounts/send_login_email', data={'email': 'user@domain.com'})
        self.assertRedirects(response, '/')

    def test_send_email_using_POST(self):
        self.send_mail_called = False

        def mock_mail(subject, body, from_email, to_list):
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list

        accounts.views.send_mail = mock_mail

        self.client.post('/accounts/send_login_email',
                         data={'email': 'user@domain.com'})

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for to-do app')
        self.assertEqual(self.from_email, 'noreply@todoapp')
        self.assertEqual(self.to_list, ['user@domain.com'])
