import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from apps.catalog.models import Product

# URLs de imágenes de Unsplash (alta calidad, libres de uso)
images = {
    'Audífonos Inalámbricos': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
    'Camiseta Deportiva': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80',
    'Laptop Gaming': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800&q=80',
    'Zapatillas Running': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80',
    'Libro de Python': 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=800&q=80',
    'Smartwatch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
    'Jeans Clásicos': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80',
    'Cafetera Eléctrica': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&q=80',
    'Bicicleta Montaña': 'https://images.unsplash.com/photo-1576435728678-68d0fbf94e91?w=800&q=80',
    'Mochila Urbana': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80',
    'Mouse Gamer': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=800&q=80',
    'Vestido Elegante': 'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=800&q=80',
    'Licuadora': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&q=80',
    'Balón de Fútbol': 'https://images.unsplash.com/photo-1614632537087-885ce4ccc346?w=800&q=80',
    'Tablet 10"': 'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=800&q=80',
    'Teclado Mecánico': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80',
    'Bufanda de Lana': 'https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=800&q=80',
    'Juego de Sábanas': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80',
    'Raqueta de Tenis': 'https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=800&q=80',
    'Cámara Digital': 'https://images.unsplash.com/photo-1606980628377-c1e77b73ccf3?w=800&q=80',
    'Chaqueta de Cuero': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&q=80',
    'Lámpara de Mesa': 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=800&q=80',
    'Pelota de Básquet': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800&q=80',
    'Parlante Bluetooth': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&q=80',
    'Gorra Deportiva': 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=800&q=80',
}

# Actualizar productos con imágenes
count = 0
for product in Product.objects.all():
    if product.name in images:
        product.image = images[product.name]
        product.save()
        count += 1
        print(f'✅ Imagen actualizada: {product.name}')

print(f'\n🎉 Total de productos actualizados: {count}')
