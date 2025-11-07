from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Elimina el usuario Ivanandres05'

    def handle(self, *args, **options):
        username = 'Ivanandres05'
        
        try:
            user = User.objects.get(username=username)
            email = user.email
            
            self.stdout.write(f"Usuario encontrado: {username} ({email})")
            user.delete()
            
            self.stdout.write(self.style.SUCCESS(f'✅ Usuario {username} eliminado exitosamente'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Usuario {username} no existe'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
