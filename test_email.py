"""
Script para probar el envío de emails en producción
Ejecutar: python test_email.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.prod')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("TEST DE CONFIGURACIÓN DE EMAIL")
print("=" * 60)

print(f"\n📧 EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"📧 EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"📧 EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"📧 EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"📧 EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"📧 EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else '(vacío)'}")
print(f"📧 DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

print("\n" + "=" * 60)

if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
    print("⚠️  ADVERTENCIA: EMAIL_BACKEND está en modo CONSOLE")
    print("   Los emails NO se enviarán, solo se imprimirán en consola")
    print("\n💡 Solución: Configura estas variables de entorno en Render:")
    print("   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
    print("   EMAIL_HOST=smtp.gmail.com")
    print("   EMAIL_PORT=587")
    print("   EMAIL_USE_TLS=True")
    print(f"   EMAIL_HOST_USER=ivanandreshernandezc@gmail.com")
    print(f"   EMAIL_HOST_PASSWORD=yfwdvfuwqmpgkrdv")
elif settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
    print("✅ EMAIL_BACKEND configurado para SMTP")
    
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("❌ ERROR: EMAIL_HOST_USER o EMAIL_HOST_PASSWORD están vacíos")
    else:
        print("✅ Credenciales configuradas")
        
        print("\n🧪 Intentando enviar email de prueba...")
        try:
            send_mail(
                subject='Test - Flash Marketplace',
                message='Este es un email de prueba desde el sistema de recuperación de contraseña.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            print("✅ ¡Email enviado exitosamente!")
            print(f"   Revisa la bandeja de entrada de: {settings.EMAIL_HOST_USER}")
        except Exception as e:
            print(f"❌ Error al enviar email: {e}")

print("=" * 60)
