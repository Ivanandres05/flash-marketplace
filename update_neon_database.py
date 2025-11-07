"""
Script para actualizar el email del usuario 'ivan' en la base de datos de producción (Neon)
y asegurar que tenga el email correcto: ivanandreshernandezc@gmail.com
"""
import os
import sys
import django

# Configurar Django para producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.prod')
django.setup()

from django.contrib.auth.models import User
from apps.accounts.models import Profile

print('\n' + '='*100)
print('🔄 ACTUALIZANDO BASE DE DATOS DE PRODUCCIÓN (NEON)')
print('='*100)

try:
    # 1. Listar todos los usuarios actuales
    print('\n📊 USUARIOS ACTUALES EN NEON:')
    print('-' * 100)
    
    all_users = User.objects.all().order_by('username')
    for user in all_users:
        try:
            profile = user.profile
            alt_email = profile.alternate_email or 'N/A'
        except:
            alt_email = 'Sin profile'
        
        print(f'  Usuario: {user.username:15} | Email: {user.email:40} | Alt: {alt_email}')
    
    print(f'\n  Total: {User.objects.count()} usuarios')
    print('-' * 100)
    
    # 2. Buscar usuario 'ivan'
    print('\n🔍 BUSCANDO USUARIO "ivan"...')
    
    try:
        ivan = User.objects.get(username='ivan')
        print(f'   ✅ Usuario encontrado:')
        print(f'      - Username: {ivan.username}')
        print(f'      - Email actual: {ivan.email}')
        print(f'      - Nombre: {ivan.first_name} {ivan.last_name}')
        print(f'      - ID: {ivan.id}')
        
        try:
            profile = ivan.profile
            print(f'      - Email alternativo: {profile.alternate_email or "N/A"}')
            print(f'      - Teléfono: {profile.phone_number or "N/A"}')
        except:
            print(f'      - Profile: No existe')
        
        # 3. Actualizar email si es necesario
        correct_email = 'ivanandreshernandezc@gmail.com'
        
        if ivan.email != correct_email:
            print(f'\n⚠️  EMAIL INCORRECTO DETECTADO')
            print(f'   Email actual: {ivan.email}')
            print(f'   Email correcto: {correct_email}')
            print(f'\n   🔄 ACTUALIZANDO EMAIL...')
            
            ivan.email = correct_email
            ivan.save()
            
            print(f'   ✅ EMAIL ACTUALIZADO CORRECTAMENTE')
            
            # Verificar actualización
            ivan.refresh_from_db()
            print(f'   ✅ Verificación: Email en BD ahora es: {ivan.email}')
        else:
            print(f'\n   ✅ EMAIL YA ES CORRECTO: {ivan.email}')
        
        # 4. Asegurar que tenga Profile
        print(f'\n📋 VERIFICANDO PROFILE...')
        profile, created = Profile.objects.get_or_create(user=ivan)
        
        if created:
            print(f'   ✅ Profile creado para usuario ivan')
        else:
            print(f'   ✅ Profile ya existe')
        
        # 5. Actualizar información adicional si es necesario
        if not ivan.first_name or not ivan.last_name:
            print(f'\n   ℹ️  Actualizando nombre completo...')
            ivan.first_name = 'Ivan'
            ivan.last_name = 'Hernandez'
            ivan.save()
            print(f'   ✅ Nombre actualizado: {ivan.first_name} {ivan.last_name}')
        
    except User.DoesNotExist:
        print(f'   ❌ Usuario "ivan" NO EXISTE en Neon')
        print(f'\n   🔧 CREANDO USUARIO "ivan"...')
        
        # Crear usuario ivan
        ivan = User.objects.create_user(
            username='ivan',
            email='ivanandreshernandezc@gmail.com',
            password='FlashMarket2025!',  # Cambia esto por la contraseña que desees
            first_name='Ivan',
            last_name='Hernandez'
        )
        
        print(f'   ✅ Usuario "ivan" creado exitosamente')
        print(f'      - Email: {ivan.email}')
        print(f'      - Contraseña: FlashMarket2025!')
        print(f'      - ⚠️  IMPORTANTE: Cambia la contraseña después de iniciar sesión')
        
        # Crear profile
        Profile.objects.create(user=ivan)
        print(f'   ✅ Profile creado')
    
    # 6. Resumen final
    print('\n' + '='*100)
    print('✅ ACTUALIZACIÓN COMPLETADA')
    print('='*100)
    
    # Mostrar estado final del usuario ivan
    ivan.refresh_from_db()
    print(f'\n📊 ESTADO FINAL DEL USUARIO "ivan":')
    print(f'   - Username: {ivan.username}')
    print(f'   - Email: {ivan.email}')
    print(f'   - Nombre: {ivan.first_name} {ivan.last_name}')
    print(f'   - Profile: {"✅ Existe" if hasattr(ivan, "profile") else "❌ No existe"}')
    
    print('\n✅ Ahora puedes usar este email para recuperar contraseña:')
    print(f'   📧 {ivan.email}')
    print('\n' + '='*100 + '\n')
    
except Exception as e:
    print(f'\n❌ ERROR CRÍTICO:')
    print(f'   Tipo: {type(e).__name__}')
    print(f'   Mensaje: {str(e)}')
    import traceback
    traceback.print_exc()
    print('\n' + '='*100 + '\n')
    sys.exit(1)
