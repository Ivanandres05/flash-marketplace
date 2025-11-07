"""
Comando para limpiar el email alternativo del usuario ivan
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Limpia el email alternativo del usuario ivan'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '='*80)
        self.stdout.write(self.style.WARNING('🧹 LIMPIANDO EMAIL ALTERNATIVO'))
        self.stdout.write('='*80 + '\n')

        try:
            from django.apps import apps
            Profile = apps.get_model('accounts', 'Profile')
            
            ivan = User.objects.get(username='ivan')
            profile = Profile.objects.get(user=ivan)
            
            if profile.alternate_email:
                self.stdout.write(f'   Email alternativo anterior: {profile.alternate_email}')
                profile.alternate_email = None
                profile.save()
                self.stdout.write(self.style.SUCCESS('   ✅ Email alternativo eliminado'))
            else:
                self.stdout.write(self.style.SUCCESS('   ✅ No había email alternativo'))
            
            self.stdout.write(f'\n   📧 Email principal: {ivan.email}')
            self.stdout.write(f'   📧 Email alternativo: {profile.alternate_email or "N/A"}')
            
            self.stdout.write('\n' + '='*80)
            self.stdout.write(self.style.SUCCESS('✅ LIMPIEZA COMPLETADA'))
            self.stdout.write('='*80 + '\n')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ ERROR: {e}'))
            raise
