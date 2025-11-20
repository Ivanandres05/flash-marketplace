#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from apps.catalog.models import Product

# Precios realistas en pesos colombianos
precios_cop = {
    'Smartphone Galaxy X': 3_600_000,
    'Laptop Pro 15"': 5_200_000,
    'Auriculares Bluetooth': 320_000,
    'Tablet 10 pulgadas': 1_400_000,
    'Smartwatch Fit': 800_000,
    'Zapatillas Running Pro': 360_000,
    'Jeans Clásicos': 200_000,
    'Chaqueta de Cuero': 640_000,
    'Camisa Formal': 160_000,
    'Vestido de Verano': 280_000,
    'Cafetera Automática': 520_000,
    'Juego de Sartenes': 360_000,
    'Aspiradora Robot': 1_200_000,
    'Licuadora Potente': 320_000,
    'Lámpara LED Inteligente': 184_000,
    'Bicicleta de Montaña': 2_400_000,
    'Mancuernas Ajustables': 520_000,
    'Yoga Mat Premium': 120_000,
    'Balón de Fútbol': 100_000,
    'Raqueta de Tenis': 360_000,
    'El Programador Pragmático': 140_000,
    'Cien Años de Soledad': 80_000,
    'Sapiens': 120_000,
    'Hábitos Atómicos': 100_000,
    'El Principito': 60_000,
    'iphone': 4_000_000,
}

print('=== ESTABLECIENDO PRECIOS CORRECTOS EN PESOS COLOMBIANOS ===\n')

products = Product.objects.all()
actualizados = 0

for product in products:
    if product.name in precios_cop:
        precio_nuevo = precios_cop[product.name]
        product.price = precio_nuevo
        product.save()
        print(f'✓ {product.name}: ${precio_nuevo:,} COP')
        actualizados += 1

print(f'\n✅ {actualizados} productos actualizados con precios en pesos colombianos')
