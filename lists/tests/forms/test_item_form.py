from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import Item, List


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter an item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_lines(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_method_handles_saving_to_list(self):
        lst = List.objects.create()
        form = ItemForm(
            data={'text': 'A new item to be saved using form save method'})
        new_item = form.save(lst)

        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(
            new_item.text, 'A new item to be saved using form save method')
        self.assertEqual(new_item.lst, lst)
