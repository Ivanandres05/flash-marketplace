"""
Script para eliminar el usuario Ivanandres05
Ejecutar: python manage.py shell < delete_user.py
"""

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='Ivanandres05')
    print(f"Usuario encontrado: {user.username} ({user.email})")
    
    # Eliminar usuario
    user.delete()
    print(f"✅ Usuario {user.username} eliminado exitosamente")
    
except User.DoesNotExist:
    print("❌ Usuario Ivanandres05 no existe")
except Exception as e:
    print(f"❌ Error: {e}")
