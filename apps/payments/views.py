from django.shortcuts import render
from django.http import JsonResponse
from .models import Payment
from .services import PaymentService

def create_payment(request):
    if request.method == 'POST':
        # Logic to create a payment
        payment_data = request.POST
        payment = PaymentService.create_payment(payment_data)
        return JsonResponse({'payment_id': payment.id}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def payment_status(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        return JsonResponse({'status': payment.status}, status=200)
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=404)

def list_payments(request):
    payments = Payment.objects.all()
    return render(request, 'payments/list.html', {'payments': payments})