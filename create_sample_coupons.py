"""
Script para crear cupones de ejemplo
Ejecutar con: python manage.py shell < create_sample_coupons.py
"""
from apps.orders.models import Coupon
from django.utils import timezone
from datetime import timedelta

# Limpiar cupones existentes (opcional)
Coupon.objects.all().delete()

# Crear cupones de ejemplo
cupones = [
    {
        'code': 'FLASH10',
        'description': '10% de descuento en tu primera compra',
        'discount_type': 'percentage',
        'discount_value': 10,
        'min_purchase_amount': 50000,
        'max_discount_amount': 50000,
        'valid_from': timezone.now(),
        'valid_to': timezone.now() + timedelta(days=30),
        'usage_limit': 100,
        'usage_limit_per_user': 1,
        'is_active': True
    },
    {
        'code': 'BIENVENIDO',
        'description': '$20,000 COP de descuento para nuevos usuarios',
        'discount_type': 'fixed',
        'discount_value': 20000,
        'min_purchase_amount': 100000,
        'valid_from': timezone.now(),
        'valid_to': timezone.now() + timedelta(days=60),
        'usage_limit': 50,
        'usage_limit_per_user': 1,
        'is_active': True
    },
    {
        'code': 'FLASH25',
        'description': '25% de descuento en compras mayores a $200,000',
        'discount_type': 'percentage',
        'discount_value': 25,
        'min_purchase_amount': 200000,
        'max_discount_amount': 100000,
        'valid_from': timezone.now(),
        'valid_to': timezone.now() + timedelta(days=15),
        'usage_limit': 30,
        'usage_limit_per_user': 2,
        'is_active': True
    },
    {
        'code': 'NAVIDAD2025',
        'description': '30% de descuento especial de Navidad',
        'discount_type': 'percentage',
        'discount_value': 30,
        'min_purchase_amount': 150000,
        'max_discount_amount': 150000,
        'valid_from': timezone.now(),
        'valid_to': timezone.now() + timedelta(days=45),
        'usage_limit': None,  # Sin límite
        'usage_limit_per_user': 3,
        'is_active': True
    },
    {
        'code': 'MEGA50',
        'description': '$50,000 COP OFF en compras de $300,000 o más',
        'discount_type': 'fixed',
        'discount_value': 50000,
        'min_purchase_amount': 300000,
        'valid_from': timezone.now(),
        'valid_to': timezone.now() + timedelta(days=20),
        'usage_limit': 20,
        'usage_limit_per_user': 1,
        'is_active': True
    }
]

for cupon_data in cupones:
    cupon = Coupon.objects.create(**cupon_data)
    print(f'✅ Cupón creado: {cupon.code}')

print(f'\n🎉 Total de cupones creados: {Coupon.objects.count()}')
