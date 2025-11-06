from django.test import TestCase
from .models import Payment

class PaymentModelTest(TestCase):

    def setUp(self):
        self.payment = Payment.objects.create(
            amount=100.00,
            method='Credit Card',
            status='Completed'
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.amount, 100.00)
        self.assertEqual(self.payment.method, 'Credit Card')
        self.assertEqual(self.payment.status, 'Completed')

    def test_payment_str(self):
        self.assertEqual(str(self.payment), f'Payment {self.payment.id} - {self.payment.amount}')