# 📧 Configuración de Gmail API para Flash Marketplace

## 🎯 Por qué Gmail API en lugar de SMTP

**Render bloquea el puerto 587** (SMTP) por razones de seguridad. Gmail API usa HTTPS y funciona perfectamente.

## 📋 Pasos para Configurar Gmail API

### 1️⃣ Crear Proyecto en Google Cloud Console

1. Ir a: https://console.cloud.google.com/
2. Crear un nuevo proyecto: **"Flash Marketplace Email"**
3. Esperar a que se cree el proyecto

### 2️⃣ Habilitar Gmail API

1. En el proyecto, ir a **"APIs & Services" → "Library"**
2. Buscar **"Gmail API"**
3. Hacer clic en **"Enable"** (Habilitar)

### 3️⃣ Crear Credenciales OAuth 2.0

1. Ir a **"APIs & Services" → "Credentials"**
2. Hacer clic en **"Create Credentials" → "OAuth client ID"**
3. Si te pide configurar pantalla de consentimiento:
   - Hacer clic en **"Configure Consent Screen"**
   - Tipo: **External**
   - App name: **Flash Marketplace**
   - User support email: **ivanandreshernandezc@gmail.com**
   - Developer contact: **ivanandreshernandezc@gmail.com**
   - Guardar y continuar
   - En "Scopes": agregar `https://www.googleapis.com/auth/gmail.send`
   - Guardar y continuar
   - En "Test users": agregar **ivanandreshernandezc@gmail.com**
   - Guardar

4. Volver a **"Credentials" → "Create Credentials" → "OAuth client ID"**
5. Application type: **Desktop app**
6. Name: **Flash Email Sender**
7. Hacer clic en **"Create"**
8. **Descargar** el archivo JSON (credentials.json)

### 4️⃣ Autorizar la Aplicación (Local)

En tu computadora local:

```bash
cd c:/Users/ivana/OneDrive/Desktop/Flash
python
```

Luego en Python:

```python
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import base64

# Scopes necesarios
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Ruta al archivo descargado
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',  # Archivo que descargaste
    SCOPES
)

# Esto abrirá el navegador para autorizar
creds = flow.run_local_server(port=0)

# Guardar credenciales
creds_dict = {
    'token': creds.token,
    'refresh_token': creds.refresh_token,
    'token_uri': creds.token_uri,
    'client_id': creds.client_id,
    'client_secret': creds.client_secret,
    'scopes': creds.scopes
}

# Convertir a base64 para variable de entorno
creds_json = json.dumps(creds_dict)
creds_base64 = base64.b64encode(creds_json.encode()).decode()

print("\n" + "="*60)
print("COPIA ESTE VALOR PARA RENDER:")
print("="*60)
print(creds_base64)
print("="*60)
```

### 5️⃣ Configurar en Render

1. Ir a: https://dashboard.render.com
2. Seleccionar tu servicio **"flash-marketplace"**
3. Ir a pestaña **"Environment"**
4. Agregar nueva variable:
   ```
   Key: GMAIL_CREDENTIALS_BASE64
   Value: [pegar el valor base64 que copiaste]
   ```
5. Guardar cambios
6. Render redesplegar automáticamente

### 6️⃣ Probar

1. Ir a: https://flash-marketplace.onrender.com/cuentas/solicitar-recuperacion/
2. Ingresar tu email
3. ¡Deberías recibir el código en segundos!

## 🔧 Configuración Local (Desarrollo)

Para desarrollo local, puedes seguir usando Gmail SMTP con App Password:

En `.env`:
```properties
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=ivanandreshernandezc@gmail.com
EMAIL_HOST_PASSWORD=qnndnwjglmtkiyir
```

O para ver emails en consola:
```properties
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## 📝 Notas Importantes

- **Gmail API** funciona en Render (usa HTTPS, no puerto 587)
- **SMTP** no funciona en Render (puerto bloqueado)
- **Las credenciales se refrescan automáticamente** con el refresh_token
- **No necesitas regenerar** las credenciales cada vez
- **El token expira cada 7 días**, pero se refresca automáticamente

## 🚨 Solución de Problemas

### Error: "Invalid grant"
- El refresh_token expiró (pasa después de ~6 meses sin uso)
- Solución: Repetir paso 4 para generar nuevas credenciales

### Error: "Daily limit exceeded"
- Gmail API tiene límite de 500 emails/día para apps no verificadas
- Solución: Verificar la app en Google Cloud Console

### No llega el email
- Revisar logs de Render
- Verificar que GMAIL_CREDENTIALS_BASE64 esté configurado
- Revisar carpeta de SPAM

## ✨ Ventajas de Gmail API

✅ Funciona en Render (HTTPS en lugar de puerto 587)
✅ Más confiable que SMTP
✅ Mejor deliverability (menos SPAM)
✅ Límite de 500 emails/día (suficiente para tu proyecto)
✅ Gratis para siempre
✅ No requiere tarjeta de crédito
✅ 100% Google, sin servicios de terceros
