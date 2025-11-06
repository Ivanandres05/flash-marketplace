from django.test import TestCase
from .models import Search

class SearchModelTest(TestCase):

    def setUp(self):
        self.search = Search.objects.create(query="test query")

    def test_search_creation(self):
        self.assertEqual(self.search.query, "test query")

    def test_search_str(self):
        self.assertEqual(str(self.search), "test query")