"""
Management command para actualizar el usuario ivan en la base de datos
Este comando se ejecutará durante el deploy
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import Profile


class Command(BaseCommand):
    help = 'Actualiza el email del usuario ivan a ivanandreshernandezc@gmail.com'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '='*80)
        self.stdout.write(self.style.WARNING('🔄 ACTUALIZANDO USUARIO IVAN EN BASE DE DATOS'))
        self.stdout.write('='*80 + '\n')

        try:
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
                # Usuario creado, establecer contraseña
                ivan.set_password('FlashMarket2025!')
                ivan.save()
                self.stdout.write(self.style.SUCCESS('✅ Usuario "ivan" CREADO exitosamente'))
                self.stdout.write(f'   Email: {ivan.email}')
                self.stdout.write(f'   Password temporal: FlashMarket2025!')
                self.stdout.write(self.style.WARNING('   ⚠️  CAMBIA LA CONTRASEÑA después de iniciar sesión'))
            else:
                # Usuario existe, verificar/actualizar email
                if ivan.email != 'ivanandreshernandezc@gmail.com':
                    self.stdout.write(self.style.WARNING(f'⚠️  Email anterior: {ivan.email}'))
                    ivan.email = 'ivanandreshernandezc@gmail.com'
                    ivan.save()
                    self.stdout.write(self.style.SUCCESS('✅ Email ACTUALIZADO a: ivanandreshernandezc@gmail.com'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'✅ Email ya correcto: {ivan.email}'))
                
                # Actualizar nombre si está vacío
                if not ivan.first_name:
                    ivan.first_name = 'Ivan'
                    ivan.last_name = 'Hernandez'
                    ivan.save()
                    self.stdout.write(self.style.SUCCESS('✅ Nombre actualizado'))

            # Asegurar que tenga profile
            profile, profile_created = Profile.objects.get_or_create(user=ivan)
            if profile_created:
                self.stdout.write(self.style.SUCCESS('✅ Profile creado'))
            else:
                self.stdout.write(self.style.SUCCESS('✅ Profile verificado'))

            # Resumen final
            self.stdout.write('\n' + '='*80)
            self.stdout.write(self.style.SUCCESS('✅ ACTUALIZACIÓN COMPLETADA'))
            self.stdout.write('='*80)
            self.stdout.write(f'\n📊 Estado del usuario:')
            self.stdout.write(f'   Username: {ivan.username}')
            self.stdout.write(f'   Email: {ivan.email}')
            self.stdout.write(f'   Nombre: {ivan.first_name} {ivan.last_name}')
            self.stdout.write(f'   Profile: {"✅" if hasattr(ivan, "profile") else "❌"}')
            self.stdout.write('\n' + '='*80 + '\n')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ ERROR: {type(e).__name__}: {e}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            raise
