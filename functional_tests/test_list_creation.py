from .base_tests import FunctionalTestSetup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTestSetup):
    '''A user story'''

    def test_can_start_list_and_retrieve_later(self):

        # Can checkout homepage
        # live_server_url is used instead of hard-coded address like
        # localhost:8000
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
        inputbox.send_keys('TO-DO ITEM FROM SECOND USER 1')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: TO-DO ITEM FROM SECOND USER 1')

        # Second user has his own URL
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')
        self.assertNotEqual(second_user_list_url, first_user_list_url)

        # Recheck what is present in second user's list
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('TO-DO ITEM FROM FIRST USER 1', body_text)
        self.assertIn('TO-DO ITEM FROM SECOND USER 1', body_text)
