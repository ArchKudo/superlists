from .base_tests import FunctionalTestSetup
from django.core import mail
from selenium.webdriver.common.keys import Keys
import re


TEST_EMAIL = 'exshir@nbox.notif.me'
SUBJECT = 'Your login link for To-do app MVC'


class LoginTest(FunctionalTestSetup):

    def test_can_get_email_link_to_login(self):
        # Can checkout homepage
        self.browser.get(self.live_server_url)

        # Can enter email and hit enter in email inputbox
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Display succesfully sent email
        self.wait_for(lambda: self.assertIn(
            'Check your email for login link',
            self.browser.find_element_by_tag_name('body').text))

        # email found in mailbox
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # email contains url link
        self.assertIn('Use this link to login:', email.body)
        url_found = re.search(r'http://.+/.+$', email.body)
        if not url_found:
            self.fail(f'Login url not found in {email.body}')
        url = url_found.group(0)
        self.assertIn(self.live_server_url, url)

        # Can go to site using link
        self.browser.get(url)

        # User is logged in
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Logout'))

        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # User can log out
        self.browser.find_element_by_link_text('Logout').click()

        self.wait_for(
            lambda: self.browser.find_element_by_name('email'))

        navbar = self.browser.find_element_by_css_selector('.navbar')

        self.assertNotIn(TEST_EMAIL, navbar.text)
