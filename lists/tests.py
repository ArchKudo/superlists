from django.test import TestCase
from lists.models import Item, List

# Create your tests here.


class HomePageTest(TestCase):

    def test_root_uses_home_template(self):
        # TestCase.client is used for get/post requests
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_save_items_only_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


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


class ListViewTest(TestCase):

    def test_list_page_uses_list_template(self):
        response = self.client.get('/lists/first_list/')
        self.assertTemplateUsed(response, 'lists.html')

    def test_list_page_can_save_POST_request(self):
        self.client.post('/lists/new_list/',
                         data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_list_page_redirects_after_POST_request(self):
        response = self.client.post(
            '/lists/new_list/', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/first_list/')

    def test_first_list_page_displays_all_items(self):
        lst = List.objects.create()
        Item.objects.create(
            text='First list item on list page', lst=lst)
        Item.objects.create(
            text='Second list item on list page', lst=lst)

        response = self.client.get('/lists/first_list/')

        self.assertContains(response, 'First list item on list page')
        self.assertContains(response, 'Second list item on list page')
