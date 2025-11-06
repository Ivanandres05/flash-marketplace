from apps.catalog.models import Category

def categories_processor(request):
    """
    Context processor para hacer las categorías disponibles en todos los templates
    """
    return {
        'categories': Category.objects.all()[:10],
    }
