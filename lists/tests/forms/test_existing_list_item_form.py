from django.test import TestCase
from lists.forms import (ExistingListItemForm,
                         DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR)
from lists.models import Item, List


class ExisitingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        lst = List.objects.create()
        form = ExistingListItemForm(lst=lst)
        self.assertIn('placeholder="Enter an item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        lst = List.objects.create()
        form = ExistingListItemForm(lst=lst, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        lst = List.objects.create()
        Item.objects.create(lst=lst, text='Unique Item')
        form = ExistingListItemForm(lst=lst, data={'text': 'Unique Item'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        lst = List.objects.create()
        form = ExistingListItemForm(lst=lst, data={'text': 'A new item'})
        new_item = form.save()
        self.assertEqual(Item.objects.all()[0], new_item)
