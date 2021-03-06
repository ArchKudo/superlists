from .base_tests import FunctionalTestSetup


class LayoutAndStylingTest(FunctionalTestSetup):

    def test_layout_styling(self):
        self.browser.get(self.live_server_url)

        # Window is 1024 x 768
        self.browser.set_window_size(1024, 768)

        inputbox = self.get_item_input_box()
        # Inputbox is at centre of the screen
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=100)
