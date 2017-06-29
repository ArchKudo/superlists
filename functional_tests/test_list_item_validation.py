from .base_tests import FunctionalTestSetup
from unittest import skip


class ItemValidationTest(FunctionalTestSetup):

    @skip
    def test_cannot_add_empty_list_items(self):
        # Try submitting blank items by pressing ENTER

        # Refresh page to show warning message
        #
        # Try submitting some text
        #
        # Submit another blank item
        #
        # Recieve similar warning message
        #
        self.fail('Write tests')
