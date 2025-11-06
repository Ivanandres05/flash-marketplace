#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from apps.catalog.models import Product

# Obtener todos los productos
products = Product.objects.all()
print(f'Total de productos: {products.count()}\n')

# Tasa de cambio: 1 USD = 4000 COP
tasa_cambio = 4000

print('=== ACTUALIZANDO PRECIOS A PESOS COLOMBIANOS ===\n')

for product in products:
    precio_anterior = product.price
    # Convertir a pesos colombianos y redondear a miles
    precio_nuevo = round(precio_anterior * tasa_cambio, -3)
    product.price = precio_nuevo
    product.save()
    print(f'✓ {product.name[:50]}')
    print(f'  Antes: ${precio_anterior:,.2f} USD')
    print(f'  Ahora: ${precio_nuevo:,.0f} COP\n')

print(f'\n✅ Todos los {products.count()} productos actualizados a pesos colombianos (COP)')
print('💰 Tasa de cambio usada: 1 USD = 4,000 COP')
