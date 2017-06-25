from django.test import TestCase
from lists.models import Item

# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')  # Client is used for get/post requests
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


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
