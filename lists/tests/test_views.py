from django.test import TestCase
from lists.forms import ItemForm
from lists.models import Item, List
from lists.forms import EMPTY_ITEM_ERROR
from django.utils.html import escape


class HomePageTest(TestCase):
    '''Tests home page view'''

    def test_uses_home_template(self):
        # TestCase.client is used for get/post requests
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListPageTest(TestCase):
    '''Tests new list page view'''

    def test_can_save_post_request(self):
        self.client.post('/lists/new_list/',
                         data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'A new list item')

    def test_redirect_after_POST(self):
        response = self.client.post(
            '/lists/new_list/', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new_list/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_in_home_page(self):
        response = self.client.post('/lists/new_list/', data={'text': ''})
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new_list/', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_items_are_not_saved(self):
        self.client.post('/lists/new_list/', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_display_item_form(self):
        lst = List.objects.create()
        response = self.client.get(f'/lists/{lst.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')


class ListPageTest(TestCase):
    '''Test list page view'''

    def post_invalid_input(self):
        lst = List.objects.create()
        return self.client.post(f'/lists/{lst.id}/', data={'text': ''})

    def test_invalid_input_saves_nothing_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists.html')

    def test_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_uses_list_template(self):
        lst = List.objects.create()
        response = self.client.get(f'/lists/{lst.id}/')
        self.assertTemplateUsed(response, 'lists.html')

    def test_passes_correct_list_to_template(self):
        lst = List.objects.create()
        response = self.client.get(f'/lists/{lst.id}/')
        self.assertEqual(response.context['lst'], lst)

    def test_list_page_can_save_POST_request(self):
        lst = List.objects.create()

        self.client.post(f'/lists/{lst.id}/',
                         data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.lst, lst)

    def test_list_page_redirects_after_POST_request(self):
        lst = List.objects.create()

        response = self.client.post(
            f'/lists/{lst.id}/', data={'text': 'A new list item'})

        self.assertRedirects(response, f'/lists/{lst.id}/')

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

    def test_validation_error_are_on_list_page(self):
        lst = List.objects.create()
        response = self.client.post(
            f'/lists/{lst.id}/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


class NewListPageItemTest(TestCase):
    '''Test add item view'''

    def test_can_save_POST_request_to_exisiting_list(self):
        lst = List.objects.create()

        self.client.post(f'/lists/{lst.id}/',
                         data={'text': 'A new item for list'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text,
                         'A new item for list')
        self.assertEqual(Item.objects.first().lst, lst)

    def test_redirect_to_list_view(self):
        lst = List.objects.create()
        response = self.client.post(
            f'/lists/{lst.id}/',
            data={'text': 'A new item for existing list'})
        self.assertRedirects(response, f'/lists/{lst.id}/')
