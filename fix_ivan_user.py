"""
Script simple para actualizar usuario ivan - ejecutar en Render Shell
"""
from django.contrib.auth.models import User
from apps.accounts.models import Profile

# Buscar o crear usuario ivan
ivan, created = User.objects.get_or_create(
    username='ivan',
    defaults={
        'email': 'ivanandreshernandezc@gmail.com',
        'first_name': 'Ivan',
        'last_name': 'Hernandez'
    }
)

if created:
    ivan.set_password('FlashMarket2025!')
    ivan.save()
    print(f'✅ Usuario ivan CREADO')
    print(f'   Email: {ivan.email}')
    print(f'   Password: FlashMarket2025!')
else:
    # Actualizar email si es diferente
    if ivan.email != 'ivanandreshernandezc@gmail.com':
        print(f'⚠️ Email anterior: {ivan.email}')
        ivan.email = 'ivanandreshernandezc@gmail.com'
        ivan.save()
        print(f'✅ Email ACTUALIZADO a: {ivan.email}')
    else:
        print(f'✅ Email ya correcto: {ivan.email}')

# Asegurar que tenga profile
profile, created = Profile.objects.get_or_create(user=ivan)
if created:
    print(f'✅ Profile creado')
else:
    print(f'✅ Profile ya existe')

print(f'\n📊 Usuario ivan:')
print(f'   Username: {ivan.username}')
print(f'   Email: {ivan.email}')
print(f'   Nombre: {ivan.first_name} {ivan.last_name}')
