import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.base')
django.setup()

from django.contrib.auth.models import User

print('\n' + '='*100)
print('USUARIOS EN LA BASE DE DATOS LOCAL')
print('='*100)

for user in User.objects.all().order_by('username'):
    try:
        profile = user.profile
        alt_email = profile.alternate_email or 'N/A'
    except:
        alt_email = 'No profile'
    
    print(f'Usuario: {user.username:15} | Email principal: {user.email:40} | Email alternativo: {alt_email}')

print('='*100)
print(f'Total de usuarios: {User.objects.count()}')
print('='*100 + '\n')
