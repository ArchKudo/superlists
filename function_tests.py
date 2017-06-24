from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, table_id, row_text):
        table = self.browser.find_element_by_id(table_id)
        rows = table.find_element_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def enter_item(self, inputbox, input_text):
        inputbox.send_keys(input_text)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

    def test_can_start_list(self):
        # A user story

        # Can checkout homepage
        self.browser.get('http://localhost:8000')

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
        self.enter_item(inputbox, 'TO-DO ITEM 1')
        self.enter_item(inputbox, 'TO-DO ITEM 2')

        # New to-do item is correctly displayed
        self.check_for_row_in_list_table('id_list_table', '1: TO-DO ITEM 1')
        self.check_for_row_in_list_table('2: TO-DO ITEM 2')

        self.fail('Finished Test!')  # Delibrately fail


if __name__ == '__main__':
    unittest.main(warnings='ignore')
