from django.test import TestCase
from lists.forms import ItemForm


class HomePageTest(TestCase):
    '''Tests home page view'''

    def test_uses_home_template(self):
        # TestCase.client is used for get/post requests
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)
