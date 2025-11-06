from apps.catalog.models import Category
from django.templatetags.static import static
import os

def categories_processor(request):
    """
    Context processor para hacer las categorías disponibles en todos los templates
    """
    return {
        'categories': Category.objects.all()[:10],
    }

def get_product_image_url(image_field):
    """
    Helper para obtener URL de imagen de producto.
    Busca en static/products/ como fallback.
    """
    if not image_field:
        return static('img/no-image.png')
    
    try:
        # Si el archivo existe en media, usar su URL
        if hasattr(image_field, 'url'):
            return image_field.url
    except:
        pass
    
    # Fallback: buscar en static/products/
    filename = os.path.basename(str(image_field))
    return static(f'products/{filename}')
