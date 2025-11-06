from django import template
from django.templatetags.static import static
import os

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica el valor por el argumento"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def product_image_url(image_field):
    """
    Devuelve la URL correcta para imágenes de productos.
    Siempre busca en static/products/ en producción.
    """
    if not image_field:
        # Imagen por defecto
        return "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"
    
    # Extraer solo el nombre del archivo
    try:
        if hasattr(image_field, 'name'):
            filename = os.path.basename(image_field.name)
        else:
            filename = os.path.basename(str(image_field))
        
        # Retornar URL desde static
        return static(f'products/{filename}')
    except Exception as e:
        # Si algo falla, retornar imagen por defecto
        return "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"
