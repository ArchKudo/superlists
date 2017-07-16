from django.test import TestCase


class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login?token=xyzzyspoonshift1')
        self.assertRedirects(response, '/')
