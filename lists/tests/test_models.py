from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


class ListAndItemModelsTest(TestCase):
    '''Tests different models present in models.py'''

    def test_saving_retrieving_items(self):
        lst = List()
        lst.save()

        first_item = Item()
        first_item.text = 'The first item'
        first_item.lst = lst
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.lst = lst
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, lst)

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        self.assertEqual(saved_item[0].text, 'The first item')
        self.assertEqual(saved_item[1].text, 'The second item')

        self.assertEqual(saved_item[0].lst, lst)
        self.assertEqual(saved_item[1].lst, lst)

    def test_cannot_save_empty_items(self):
        lst = List.objects.create()
        item = Item(lst=lst, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        lst = List.objects.create()
        self.assertEqual(lst.get_absolute_url(), f'/lists/{lst.id}/')
