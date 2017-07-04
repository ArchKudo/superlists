from .base_tests import FunctionalTestSetup
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTestSetup):

    def test_disallow_empty_list_items(self):

        # Try Submititting blank items by pressing ENTER
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Browser returns error
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'))

        # Trying submitting some text removes error
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'))

        # Items can be submitted successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Submit another blank item
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'))

        # Enter new items to remove error warnings
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_disallow_adding_duplicate_items(self):

        # Create a new list
        self.browser.get(self.live_server_url)

        # Add a unique item
        self.get_item_input_box().send_keys('Unique item')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Unique item')

        # Try re-adding the same item
        self.get_item_input_box().send_keys('Unique item')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Browser returns error
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(
                '.has-error').text, 'Cannot add duplicate items!'))

    def test_error_messages_are_cleared_on_input(self):

        # Start the browser
        self.browser.get(self.live_server_url)

        # Add a new item
        self.get_item_input_box().send_keys('Unique Item')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Check for newly added item in table
        self.wait_for_row_in_list_table('1: Unique Item')

        # Re-enter the same item
        self.get_item_input_box().send_keys('Unique Item')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Check whether it raises error
        self.wait_for(lambda: self.assertTrue(
            self.browser.find_element_by_css_selector(
                '.has-error').is_displayed()))

        # Typing in the inputbox removes the error
        self.get_item_input_box().send_keys('a')

        # Check whether the error disappears
        self.wait_for(lambda: self.assertFalse(
            self.browser.find_element_by_css_selector(
                '.has-error').is_displayed()))
