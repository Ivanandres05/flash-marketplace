"""
Script para verificar y actualizar el email del usuario en la base de datos de producción (Neon)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.prod')
django.setup()

from django.contrib.auth.models import User

print('\n' + '='*100)
print('VERIFICANDO USUARIOS EN NEON (PRODUCCIÓN)')
print('='*100)

try:
    users = User.objects.all().order_by('username')
    
    for user in users:
        try:
            profile = user.profile
            alt_email = profile.alternate_email or 'N/A'
        except:
            alt_email = 'No profile'
        
        print(f'Usuario: {user.username:15} | Email principal: {user.email:40} | Email alternativo: {alt_email}')
    
    print('='*100)
    print(f'Total de usuarios: {User.objects.count()}')
    print('='*100)
    
    # Verificar usuario 'ivan' específicamente
    print('\n🔍 VERIFICANDO USUARIO "ivan":')
    try:
        ivan = User.objects.get(username='ivan')
        print(f'   Username: {ivan.username}')
        print(f'   Email principal: {ivan.email}')
        print(f'   Nombre: {ivan.first_name} {ivan.last_name}')
        try:
            print(f'   Email alternativo: {ivan.profile.alternate_email or "N/A"}')
        except:
            print(f'   Email alternativo: No profile')
        
        # Preguntar si desea actualizar
        print('\n¿Deseas actualizar el email a ivanandreshernandezc@gmail.com? (s/n)')
        respuesta = input('> ').strip().lower()
        
        if respuesta == 's':
            ivan.email = 'ivanandreshernandezc@gmail.com'
            ivan.save()
            print('✅ Email actualizado correctamente en Neon!')
        else:
            print('❌ No se realizaron cambios')
            
    except User.DoesNotExist:
        print('   ⚠️ Usuario "ivan" NO existe en Neon')
        print('\n¿Deseas crear el usuario "ivan"? (s/n)')
        respuesta = input('> ').strip().lower()
        
        if respuesta == 's':
            password = input('Contraseña para el usuario: ').strip()
            User.objects.create_user(
                username='ivan',
                email='ivanandreshernandezc@gmail.com',
                password=password,
                first_name='Ivan',
                last_name='Hernandez'
            )
            print('✅ Usuario "ivan" creado exitosamente en Neon!')
        else:
            print('❌ No se creó el usuario')
    
except Exception as e:
    print(f'\n❌ ERROR: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()

print('\n')
