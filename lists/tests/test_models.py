from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


class ListAndItemModelsTest(TestCase):
    '''Tests different models present in models.py'''

    def test_item_is_related_to_list(self):
        lst = List.objects.create()
        item = Item()
        item.lst = lst
        item.save()
        self.assertIn(item, lst.item_set.all())

    def test_cannot_save_empty_items(self):
        lst = List.objects.create()
        item = Item(lst=lst, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        lst = List.objects.create()
        Item.objects.create(lst=lst, text='Unique Item')
        with self.assertRaises(ValidationError):
            item = Item(lst=lst, text='Unique Item')
            item.full_clean()

    def test_allow_same_item_in_different_lists(self):
        lst_one = List.objects.create()
        lst_two = List.objects.create()
        Item.objects.create(lst=lst_one, text='Unique Item')
        item = Item.objects.create(lst=lst_two, text='Unique Item')
        item.full_clean()

    def test_list_ordering(self):
        lst = List.objects.create()
        item_one = Item.objects.create(lst=lst, text='Item 1')
        item_two = Item.objects.create(lst=lst, text='Item 2')
        item_three = Item.objects.create(lst=lst, text='Item 3')

        self.assertEqual(list(Item.objects.all()), [
                         item_one, item_two, item_three])


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        lst = List.objects.create()
        self.assertEqual(lst.get_absolute_url(), f'/lists/{lst.id}/')


class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_string_representation(self):
        item = Item(text='Item 1')
        self.assertEqual(str(item), 'Item 1')
