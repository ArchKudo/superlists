from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

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
        time.sleep(1)

        self.check_for_row_in_list_table('1: TO-DO ITEM 1')

        # New to-do item is correctly displayed
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('TO-DO ITEM 2')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('2: TO-DO ITEM 2')
        self.check_for_row_in_list_table('1: TO-DO ITEM 1')

        self.fail('Finished Test!')  # Delibrately fail
