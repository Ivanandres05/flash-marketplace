"""
Script para verificar la configuración de límites de uso de los cupones
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from apps.orders.models import Coupon, CouponUsage

print("=" * 60)
print("VERIFICACIÓN DE CUPONES Y SUS LÍMITES DE USO")
print("=" * 60)

coupons = Coupon.objects.all()

for coupon in coupons:
    print(f"\n📋 Cupón: {coupon.code}")
    print(f"   Tipo: {coupon.get_discount_type_display()}")
    print(f"   Descuento: {coupon.discount_value}{'%' if coupon.discount_type == 'percentage' else ' COP'}")
    print(f"   Límite total de usos: {coupon.usage_limit or 'Ilimitado'}")
    print(f"   Límite por usuario: {coupon.usage_limit_per_user}")
    print(f"   Veces usado: {coupon.times_used}")
    print(f"   Estado: {'✅ Activo' if coupon.is_active else '❌ Inactivo'}")
    
    # Mostrar usos registrados
    usages = CouponUsage.objects.filter(coupon=coupon)
    print(f"   Registros de uso: {usages.count()}")
    
    if usages.exists():
        print("   Usuarios que lo han usado:")
        for usage in usages:
            print(f"      - {usage.user.username} (Orden #{usage.order.id}) - {usage.used_at.strftime('%d/%m/%Y %H:%M')}")

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print(f"Total de cupones: {coupons.count()}")
print(f"Total de usos registrados: {CouponUsage.objects.count()}")
