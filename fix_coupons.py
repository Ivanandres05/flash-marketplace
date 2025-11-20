"""
Script para actualizar y hacer válidos todos los cupones
"""
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Coupon

# Obtener la fecha actual
now = timezone.now()

# Actualizar todos los cupones para que sean válidos
cupones_actualizados = 0

for coupon in Coupon.objects.all():
    # Hacer que el cupón sea válido desde hace 1 día y válido hasta dentro de 1 año
    coupon.valid_from = now - timedelta(days=1)
    coupon.valid_to = now + timedelta(days=365)
    coupon.is_active = True
    coupon.save()
    cupones_actualizados += 1
    print(f"✅ Cupón '{coupon.code}' actualizado - Válido hasta {coupon.valid_to.strftime('%d/%m/%Y')}")

print(f"\n🎉 Total de cupones actualizados: {cupones_actualizados}")
print("\n📋 Estado de los cupones:")
print("-" * 60)

for coupon in Coupon.objects.all():
    is_valid, message = coupon.is_valid()
    status = "✅ VÁLIDO" if is_valid else "❌ INVÁLIDO"
    print(f"{status} - {coupon.code}: {message}")
    print(f"   Tipo: {coupon.get_discount_type_display()}")
    print(f"   Descuento: {coupon.discount_value}{'%' if coupon.discount_type == 'percentage' else ' COP'}")
    print(f"   Compra mínima: ${coupon.min_purchase_amount:,.0f}")
    print(f"   Usos: {coupon.times_used}/{coupon.usage_limit if coupon.usage_limit else '∞'}")
    print("-" * 60)
