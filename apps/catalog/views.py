from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category

def product_list_view(request):
    """Vista de listado de productos con filtros y ordenamiento"""
    products = Product.objects.filter(available=True).select_related('category')
    
    # Filtro por categoría
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Filtro por rango de precio
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Filtro por calificación (si existe el modelo Review)
    rating = request.GET.get('rating')
    if rating:
        try:
            from django.db.models import Avg
            from apps.reviews.models import Review
            # Anotar productos con su calificación promedio
            products = products.annotate(
                avg_rating=Avg('reviews__rating')
            ).filter(avg_rating__gte=float(rating))
        except:
            pass
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        from django.db.models import Q
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Ordenamiento
    sort_by = request.GET.get('sort', 'default')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created')
    elif sort_by == 'popular':
        # Ordenar por número de ventas o vistas (si tienes ese campo)
        products = products.order_by('-id')  # Por ahora ordenar por ID descendente
    else:
        products = products.order_by('-created')
    
    categories = Category.objects.all()
    
    # Obtener precio mínimo y máximo para el filtro
    from django.db.models import Min, Max
    price_range = Product.objects.filter(available=True).aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'selected_sort': sort_by,
        'min_price_filter': min_price,
        'max_price_filter': max_price,
        'price_range': price_range,
        'query': query,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail_view(request, slug):
    """Vista de detalle de producto"""
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # Productos relacionados de la misma categoría
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    # Reseñas del producto
    try:
        from apps.reviews.models import Review
        reviews = Review.objects.filter(product=product).select_related('user').order_by('-created_at')
    except:
        reviews = []
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'catalog/product_detail.html', context)
