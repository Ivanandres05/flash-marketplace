"""
Utilidad para enviar emails usando Gmail API
Funciona en Render (no requiere puerto SMTP 587)
"""
import base64
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings


def send_gmail_api(to_email, subject, html_content, text_content=None):
    """
    Envía un email usando Gmail API
    
    Args:
        to_email: Destinatario
        subject: Asunto del email
        html_content: Contenido HTML
        text_content: Contenido texto plano (opcional)
    
    Returns:
        bool: True si se envió exitosamente, False si falló
    """
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        # Obtener credenciales desde variable de entorno (Base64)
        creds_base64 = getattr(settings, 'GMAIL_CREDENTIALS_BASE64', '')
        
        if not creds_base64:
            print("⚠️ GMAIL_CREDENTIALS_BASE64 no configurado")
            return False
        
        # Decodificar credenciales
        creds_json = base64.b64decode(creds_base64).decode('utf-8')
        creds_dict = json.loads(creds_json)
        
        # Crear credenciales
        creds = Credentials.from_authorized_user_info(creds_dict)
        
        # Crear servicio Gmail
        service = build('gmail', 'v1', credentials=creds)
        
        # Crear mensaje
        message = MIMEMultipart('alternative')
        message['To'] = to_email
        message['From'] = settings.DEFAULT_FROM_EMAIL
        message['Subject'] = subject
        
        # Agregar contenido
        if text_content:
            part1 = MIMEText(text_content, 'plain')
            message.attach(part1)
        
        part2 = MIMEText(html_content, 'html')
        message.attach(part2)
        
        # Codificar mensaje
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Enviar
        send_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        print(f"✅ Email enviado con Gmail API - ID: {send_message['id']}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando con Gmail API: {type(e).__name__}: {e}")
        return False


def send_gmail_simple(to_email, subject, html_content, text_content=None):
    """
    Método simplificado usando App Password (para desarrollo local)
    
    NOTA: No funciona en Render por puerto 587 bloqueado
    Solo usar en desarrollo local
    """
    from django.core.mail import EmailMultiAlternatives
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content or 'Ver versión HTML',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        
        print(f"✅ Email enviado con SMTP")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando con SMTP: {type(e).__name__}: {e}")
        return False
