from django.db import models

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CREDIT_CARD', 'Credit Card'),
        ('PAYPAL', 'PayPal'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    ]

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} - {self.amount} - {self.status}"