import os
import django
import requests
from io import BytesIO
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from apps.catalog.models import Product, ProductImage

def download_image(url):
    """Descarga una imagen desde una URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
        return None
    except Exception as e:
        print(f"Error descargando imagen: {e}")
        return None

def add_images_to_products():
    """Agrega imágenes a todos los productos que no tienen"""
    products = Product.objects.all()
    
    # URLs de imágenes genéricas de productos (usando picsum.photos)
    image_categories = {
        'Electrónica': [
            'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',  # Auriculares
            'https://images.unsplash.com/photo-1588508065123-287b28e013da?w=800',  # Laptop
            'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800',  # Smartwatch
            'https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=800',  # Teclado
            'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800',  # Mouse
        ],
        'Ropa': [
            'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800',  # Camiseta
            'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800',  # Zapatos
            'https://images.unsplash.com/photo-1495105787522-5334e3ffa0ef?w=800',  # Gorra
            'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800',  # Chaqueta
            'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=800',  # Ropa
        ],
        'Hogar': [
            'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800',  # Sofá
            'https://images.unsplash.com/photo-1505693314120-0d443867891c?w=800',  # Lámpara
            'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=800',  # Silla
            'https://images.unsplash.com/photo-1581539250439-c96689b516dd?w=800',  # Decoración
            'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800',  # Cocina
        ],
        'Deportes': [
            'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800',  # Bicicleta
            'https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=800',  # Pesas
            'https://images.unsplash.com/photo-1578762560042-46ad127c95ea?w=800',  # Balón
            'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800',  # Gym
            'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=800',  # Running
        ],
        'Libros': [
            'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=800',  # Libro
            'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800',  # Biblioteca
            'https://images.unsplash.com/photo-1524578271613-d550eacf6090?w=800',  # Libros apilados
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800',  # Lectura
            'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800',  # Escritorio
        ]
    }
    
    # Imagen genérica por defecto
    default_images = [
        'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800',
        'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800',
        'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800',
        'https://images.unsplash.com/photo-1560343090-f0409e92791a?w=800',
        'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=800',
    ]
    
    count = 0
    for i, product in enumerate(products):
        # Verificar si el producto ya tiene imágenes
        if product.images.exists():
            print(f"✓ {product.name} ya tiene imágenes")
            continue
        
        # Seleccionar URL de imagen según categoría
        category_name = product.category.name if product.category else 'default'
        
        # Buscar categoría que coincida
        image_url = None
        for cat_key, urls in image_categories.items():
            if cat_key.lower() in category_name.lower():
                image_url = urls[i % len(urls)]
                break
        
        # Si no encuentra categoría, usar imagen por defecto
        if not image_url:
            image_url = default_images[i % len(default_images)]
        
        # Descargar imagen
        print(f"Descargando imagen para: {product.name}...")
        image_data = download_image(image_url)
        
        if image_data:
            # Crear ProductImage
            product_image = ProductImage(
                product=product,
                alt_text=f"{product.name}"
            )
            
            # Guardar la imagen
            filename = f"product_{product.id}_{i}.jpg"
            product_image.image.save(filename, File(image_data), save=True)
            
            print(f"✓ Imagen agregada a: {product.name}")
            count += 1
        else:
            print(f"✗ No se pudo descargar imagen para: {product.name}")
    
    print(f"\n✓ Proceso completado. {count} imágenes agregadas.")

if __name__ == '__main__':
    print("Agregando imágenes a productos...")
    print("=" * 50)
    add_images_to_products()
