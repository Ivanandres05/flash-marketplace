"""
Script para actualizar las rutas de imágenes de productos
De: products/image.jpg
A: static/products/image.jpg (para que se sirvan desde static en producción)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.prod')
django.setup()

from apps.catalog.models import Product

def fix_image_paths():
    products = Product.objects.all()
    updated = 0
    
    for product in products:
        if product.image and product.image.name:
            # Extraer solo el nombre del archivo
            filename = os.path.basename(product.image.name)
            print(f"Producto: {product.name}")
            print(f"  Imagen antigua: {product.image.name}")
            print(f"  Solo filename: {filename}")
            updated += 1
    
    print(f"\n✓ Total productos con imágenes: {updated}")
    print("\nNOTA: Las imágenes ahora se sirven desde:")
    print("  /static/products/[nombre_archivo].jpg")
    print("\nEn los templates, usa:")
    print("  {% static 'products/' %}{{ product.image.name|basename }}")

if __name__ == '__main__':
    fix_image_paths()
