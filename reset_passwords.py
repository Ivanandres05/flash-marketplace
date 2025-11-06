"""
Script para cambiar todas las contraseñas de usuarios a 'flash123'
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from django.contrib.auth.models import User

# Nueva contraseña
NEW_PASSWORD = 'flash123'

print("=" * 70)
print("CAMBIANDO CONTRASEÑAS DE TODOS LOS USUARIOS")
print("=" * 70)
print(f"\nNueva contraseña para todos: {NEW_PASSWORD}\n")

users = User.objects.all()
updated_count = 0

for user in users:
    user.set_password(NEW_PASSWORD)
    user.save()
    updated_count += 1
    print(f"✅ {user.username:20} - Contraseña actualizada")

print("\n" + "=" * 70)
print(f"COMPLETADO: {updated_count} contraseñas actualizadas")
print("=" * 70)
print(f"\nCredenciales para iniciar sesión:")
print("-" * 70)

for user in users:
    print(f"Usuario: {user.username:20} | Contraseña: {NEW_PASSWORD}")

print("\n" + "=" * 70)
print("NOTA: Todas las contraseñas son ahora: flash123")
print("=" * 70)
