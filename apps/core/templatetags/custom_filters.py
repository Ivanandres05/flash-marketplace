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
    En producción, busca en static/products/
    """
    if not image_field:
        return static('img/no-image.png')
    
    try:
        # Intentar obtener la URL del media field
        return image_field.url
    except:
        # Si falla, buscar en static/products/
        filename = os.path.basename(str(image_field))
        return static(f'products/{filename}')
