"""
Script para listar todos los usuarios registrados en Flash
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from django.contrib.auth.models import User
from apps.accounts.models import Profile, Seller

print("=" * 70)
print("USUARIOS REGISTRADOS EN FLASH")
print("=" * 70)

users = User.objects.all().order_by('-date_joined')

for user in users:
    print(f"\n{'='*70}")
    print(f"👤 Usuario: {user.username}")
    print(f"   ID: {user.id}")
    print(f"   Email: {user.email}")
    print(f"   Nombre: {user.first_name} {user.last_name}")
    print(f"   Fecha de registro: {user.date_joined.strftime('%d/%m/%Y %H:%M')}")
    print(f"   Último acceso: {user.last_login.strftime('%d/%m/%Y %H:%M') if user.last_login else 'Nunca'}")
    print(f"   Estado: {'✅ Activo' if user.is_active else '❌ Inactivo'}")
    print(f"   Staff: {'✅ Sí' if user.is_staff else '❌ No'}")
    print(f"   Superusuario: {'✅ Sí' if user.is_superuser else '❌ No'}")
    
    # Verificar si tiene perfil
    try:
        profile = user.profile
        print(f"   Teléfono: {profile.phone_number or 'No registrado'}")
    except:
        print(f"   Perfil: ❌ No tiene")
    
    # Verificar si es vendedor
    try:
        seller = Seller.objects.get(user=user)
        print(f"   🏪 Vendedor: {seller.store_name}")
        print(f"      Estado: {'✅ Verificado' if seller.is_verified else '⏳ No verificado'}")
        from apps.catalog.models import Product
        products_count = Product.objects.filter(seller=user).count()
        print(f"      Productos: {products_count}")
    except Seller.DoesNotExist:
        print(f"   Vendedor: ❌ No")

print(f"\n{'='*70}")
print(f"RESUMEN")
print(f"{'='*70}")
print(f"Total de usuarios: {users.count()}")
print(f"Usuarios activos: {User.objects.filter(is_active=True).count()}")
print(f"Administradores: {User.objects.filter(is_superuser=True).count()}")
print(f"Staff: {User.objects.filter(is_staff=True).count()}")
print(f"Vendedores: {Seller.objects.count()}")
print(f"Vendedores verificados: {Seller.objects.filter(is_verified=True).count()}")

print("\n" + "=" * 70)
print("NOTA: Las contraseñas están encriptadas y no pueden mostrarse")
print("Para cambiar una contraseña, usa: python manage.py changepassword <usuario>")
print("=" * 70)
