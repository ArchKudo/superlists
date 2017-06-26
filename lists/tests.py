from django.test import TestCase
from lists.models import Item

# Create your tests here.


class HomePageTest(TestCase):

    def test_root_uses_home_template(self):
        # TestCase.client is used for get/post requests
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_can_save_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_home_page_redirects_after_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_save_items_only_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_items(self):
        Item.objects.create(text='First list item of all list items')
        Item.objects.create(text='Second list item of all list items')

        response = self.client.get('/')

        self.assertIn('First list item of all list items',
                      response.content.decode())
        self.assertIn('Second list item of all list items',
                      response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        self.assertEqual(saved_item[0].text, 'The first item')
        self.assertEqual(saved_item[1].text, 'The second item')
