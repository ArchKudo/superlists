from django.test import TestCase
from lists.models import Item


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_string_representation(self):
        item = Item(text='Item 1')
        self.assertEqual(str(item), 'Item 1')
