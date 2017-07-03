from django.test import TestCase
from django.utils.html import escape
from lists.forms import ItemForm
from lists.models import Item, List
from lists.forms import EMPTY_ITEM_ERROR


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
