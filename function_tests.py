from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_list(self):
        # A user story

        # Can checkout homepage
        self.browser.get('http://localhost:8000')

        # Page title and header mention To-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Page has an input field with placeholder text
        inputbox = self.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter an item'
        )

        # Can add a new to-do item using ENTER key
        inputbox.send_keys('TO-DO ITEM 1')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: TO-DO ITEM 1' for row in rows)
        )

        self.fail('Finished Test!')  # Delibrately fail


if __name__ == '__main__':
    unittest.main(warnings='ignore')
