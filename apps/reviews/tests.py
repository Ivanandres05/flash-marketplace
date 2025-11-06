from django.test import TestCase
from .models import Review

class ReviewModelTest(TestCase):

    def setUp(self):
        self.review = Review.objects.create(
            title="Great Product",
            content="I really enjoyed using this product.",
            rating=5
        )

    def test_review_creation(self):
        self.assertEqual(self.review.title, "Great Product")
        self.assertEqual(self.review.content, "I really enjoyed using this product.")
        self.assertEqual(self.review.rating, 5)

    def test_review_str(self):
        self.assertEqual(str(self.review), "Great Product")