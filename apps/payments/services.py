from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Payment

def process_payment(payment_data):
    # Aquí se procesaría el pago utilizando una API de pago
    payment = Payment.objects.create(
        amount=payment_data['amount'],
        user=payment_data['user'],
        created_at=timezone.now(),
        status='processed'
    )
    return payment

def send_payment_confirmation(payment):
    subject = 'Confirmación de Pago'
    message = f'Tu pago de {payment.amount} ha sido procesado con éxito.'
    recipient_list = [payment.user.email]
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)