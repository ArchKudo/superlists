from django.test import TestCase
from lists.models import List


class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        lst = List.objects.create()
        self.assertEqual(lst.get_absolute_url(), f'/lists/{lst.id}/')
