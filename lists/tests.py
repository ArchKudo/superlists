from django.test import TestCase
from lists.models import Item, List

# Create your tests here.


class HomePageTest(TestCase):
    '''Tests home page view'''

    def test_uses_home_template(self):
        # TestCase.client is used for get/post requests
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewListPageTest(TestCase):
    '''Tests new list page view'''

    def test_can_save_post_request(self):
        self.client.post('/lists/new_list/',
                         data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirect_after_POST(self):
        response = self.client.post(
            '/lists/new_list/', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


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


class ListPageTest(TestCase):
    '''Test list page view'''

    def test_uses_list_template(self):
        lst = List.objects.create()
        response = self.client.get(f'/lists/{lst.id}/')
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
        first_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{first_list.id}/')

    def test_first_list_page_displays_all_items(self):
        lst = List.objects.create()
        Item.objects.create(
            text='First list item on list page', lst=lst)
        Item.objects.create(
            text='Second list item on list page', lst=lst)

        response = self.client.get(f'/lists/{lst.id}/')

        self.assertContains(response, 'First list item on list page')
        self.assertContains(response, 'Second list item on list page')

    def test_displays_items_only_of_specified_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Correct item 1', lst=correct_list)
        Item.objects.create(text='Correct item 2', lst=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Other list item 1', lst=other_list)
        Item.objects.create(text='Other list item 2', lst=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Correct item 1')
        self.assertContains(response, 'Correct item 2')
        self.assertNotContains(response, 'Other list item 1')
        self.assertNotContains(response, 'Other list item 2')

    def test_passes_correct_list_to_template(self):
        lst = List.objects.create()
        response = self.client.get(f'/lists/{lst.id}/')
        self.assertEqual(response.context['lst'], lst)


class NewListPageItemTest(TestCase):
    '''Test add item view'''

    def test_can_save_POST_request_to_exisiting_list(self):
        lst = List.objects.create()

        self.client.post(f'/lists/{lst.id}/add_item/',
                         data={'item_text': 'A new item for list'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text,
                         'A new item for list')
        self.assertEqual(Item.objects.first().lst, lst)

    def test_redirect_to_list_view(self):
        lst = List.objects.create()
        response = self.client.post(
            f'/lists/{lst.id}/add_item/',
            data={'item_text': 'A new item for existing list'})
        self.assertRedirects(response, f'/lists/{lst.id}/')
