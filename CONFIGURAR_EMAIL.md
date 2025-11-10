# 📧 Configuración de Email para Flash Marketplace

## 🔧 Configurar Gmail App Password

### Paso 1: Habilitar Verificación en 2 Pasos

1. Ve a tu cuenta de Google: https://myaccount.google.com/security
2. En "Cómo accedes a Google", habilita **Verificación en 2 pasos**
3. Sigue el proceso de verificación (SMS, llamada, etc.)

### Paso 2: Crear Contraseña de Aplicación

1. Una vez habilitada la verificación en 2 pasos, ve a: https://myaccount.google.com/apppasswords
2. En "Selecciona la app", elige **Mail** o **Otra (nombre personalizado)**: "Flash Marketplace"
3. En "Selecciona el dispositivo", elige **Otro** y escribe: "Render Server"
4. Haz clic en **Generar**
5. Google te mostrará una contraseña de 16 caracteres como: `abcd efgh ijkl mnop`
6. **Copia esta contraseña SIN espacios**: `abcdefghijklmnop`

### Paso 3: Configurar en Render

1. Ve a tu servicio en Render: https://dashboard.render.com
2. Selecciona tu servicio "flash-marketplace"
3. Ve a la pestaña **Environment**
4. Agrega/actualiza estas variables:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=ivanandreshernandezc@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=ivanandreshernandezc@gmail.com
```

5. Haz clic en **Save Changes**
6. Render automáticamente redesplegar á tu app

### Paso 4: Verificar

1. Ve a tu app: https://flash-marketplace.onrender.com
2. Intenta recuperar contraseña
3. Deberías recibir el email con el código en segundos

## 🔍 Solución de Problemas

### Error: "SMTPAuthenticationError"
- ✅ Verifica que la contraseña de aplicación esté sin espacios
- ✅ Asegúrate de tener verificación en 2 pasos habilitada
- ✅ Intenta generar una nueva contraseña de aplicación

### Error: "SMTPSenderRefused"
- ✅ Verifica que el email en `EMAIL_HOST_USER` sea correcto
- ✅ Asegúrate de que `DEFAULT_FROM_EMAIL` sea el mismo email

### No llega el email
- ✅ Revisa la carpeta de SPAM
- ✅ Verifica en los logs de Render que se envió sin errores
- ✅ Prueba enviando un email de prueba desde tu cuenta de Gmail primero

## 📝 Prueba Local (Opcional)

Si quieres probar emails en tu máquina local:

1. Edita `.env`:
```properties
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_PASSWORD=tu-app-password-de-16-caracteres
```

2. Reinicia el servidor de desarrollo:
```bash
python manage.py runserver
```

3. Solicita recuperación de contraseña en http://localhost:8080

## 🎯 Modo Desarrollo (Console)

Por defecto, en desarrollo local los emails se imprimen en la consola:

```properties
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Esto es útil para desarrollo sin necesidad de configurar SMTP.
