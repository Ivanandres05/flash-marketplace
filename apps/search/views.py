from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.none()
    
    return render(request, 'search/results.html', {'products': products})