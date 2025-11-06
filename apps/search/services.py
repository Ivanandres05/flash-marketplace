from django.db.models import Q
from apps.catalog.models import Product

def search_products(query):
    """
    Busca productos en la base de datos que coincidan con la consulta dada.
    """
    if not query:
        return Product.objects.none()
    
    return Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query)
    )