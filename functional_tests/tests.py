from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        MAX_WAIT = 10
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_list_and_retrieve_later(self):
        # A user story

        # Can checkout homepage
        self.browser.get(self.live_server_url)

        # Page title and header mention To-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Page has an input field with placeholder text
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter an item'
        )

        # Can add a new to-do item using ENTER key
        inputbox.send_keys('TO-DO ITEM 1')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: TO-DO ITEM 1')

        # New to-do item is correctly displayed
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('TO-DO ITEM 2')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2: TO-DO ITEM 2')
        self.wait_for_row_in_list_table('1: TO-DO ITEM 1')

        # self.fail('Finished Test!')  # Delibrately fail

    def test_different_list_url_for_multiple_user(self):
        # Can open URL and create a new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('TO-DO ITEM FROM FIRST USER 1')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: TO-DO ITEM FROM FIRST USER 1')

        # Each list has unique URL
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')

        # Quit browser
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Second user visits URL
        # Has a clean slate with no presence of first users list
        self.browser.get(self.live_server_url)
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('TO-DO ITEM FROM FIRST USER 1', body_text)

        # Second users creates new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('TO-DO ITEM FROM SECOND USER 2')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: TO-DO ITEM FROM SECOND USER 2')

        # Second user has his own URL
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/list/.+')
        self.assertNotEqual(second_user_list_url, first_user_list_url)

        body_text = self.browser.find_element_by_id('body').text
        self.assertNotIn('TO-DO ITEM FROM FIRST USER 1', body_text)
        self.assertIn('TO-DO ITEM FROM SECOND USER 2', body_text)
