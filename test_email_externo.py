"""
Test para verificar envío de email a OTRO correo diferente
Ejecutar: python test_email_externo.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.base')

# Configurar variables de entorno para usar SMTP
os.environ['EMAIL_BACKEND'] = 'django.core.mail.backends.smtp.EmailBackend'
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = '587'
os.environ['EMAIL_USE_TLS'] = 'True'
os.environ['EMAIL_HOST_USER'] = 'ivanandreshernandezc@gmail.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'yfwdvfuwqmpgkrdv'

django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("TEST DE ENVÍO A EMAIL EXTERNO")
print("=" * 60)

# CAMBIA ESTE EMAIL POR OTRO QUE TENGAS (NO ivanandreshernandezc@gmail.com)
test_email = input("\n📧 Ingresa un email DIFERENTE para probar (ejemplo: otro@gmail.com): ").strip()

if not test_email or test_email == 'ivanandreshernandezc@gmail.com':
    print("❌ ERROR: Debes usar un email DIFERENTE al que envía")
    exit(1)

print(f"\n🧪 Enviando email de prueba a: {test_email}")
print(f"📤 Desde: {settings.DEFAULT_FROM_EMAIL}")

try:
    send_mail(
        subject='Código de Recuperación - Flash Marketplace TEST',
        message='''
Hola,

Este es un email de PRUEBA del sistema de recuperación de contraseña.

Tu código de verificación es: 123456

Este es un email de prueba para verificar que el sistema funciona correctamente.

Saludos,
El equipo de Flash Marketplace
        ''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[test_email],
        fail_silently=False,
    )
    print("✅ ¡Email enviado exitosamente!")
    print(f"\n📥 Revisa la bandeja de entrada de: {test_email}")
    print("   (También revisa spam)")
except Exception as e:
    print(f"❌ Error al enviar email: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
