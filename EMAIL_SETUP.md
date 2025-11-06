# 📧 Configuración de Email para Recuperación de Contraseña

## 🚀 ESTADO ACTUAL

✅ **Sistema funcionando en modo desarrollo**
- Los emails se muestran en la **consola del servidor** (terminal)
- No necesitas configurar nada para probar
- Perfecto para desarrollo y testing

---

## 🔧 CONFIGURAR GMAIL (Para Producción)

Si quieres enviar emails reales desde Gmail, sigue estos pasos:

### 1️⃣ Habilitar Contraseñas de Aplicación en Google

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Navega a **Seguridad** → **Verificación en dos pasos** (actívala si no está)
3. Scroll abajo y busca **Contraseñas de aplicaciones**
4. Selecciona "Correo" y "Dispositivo personalizado"
5. Dale un nombre: "Flash Marketplace"
6. **Copia la contraseña de 16 caracteres** que te genera

### 2️⃣ Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # La contraseña de app de Google
```

### 3️⃣ Instalar python-decouple

```bash
.venv/Scripts/pip install python-decouple
```

### 4️⃣ Actualizar settings/base.py

Cambia estas líneas:

```python
# Línea 103-104 - CAMBIAR DE:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# A:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Línea 107-108 - CAMBIAR DE:
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'tu-email@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'tu-contraseña-app')

# A (agregar al inicio del archivo):
from decouple import config

# Y cambiar a:
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

---

## 🧪 CÓMO PROBAR

### Modo Desarrollo (Actual - Consola)

1. Inicia el servidor:
```bash
.venv/Scripts/python manage.py runserver 8080
```

2. Ve a: http://127.0.0.1:8080/cuenta/login/

3. Click en **"¿Olvidaste tu contraseña?"**

4. Ingresa un email de usuario registrado (ej: `admin@example.com`)

5. **Mira la consola del terminal** - verás el email completo con el link

6. Copia el link que aparece y pégalo en el navegador

7. Ingresa nueva contraseña y listo ✅

### Modo Producción (Gmail configurado)

1. Igual que arriba, pero el email se enviará realmente

2. Revisa tu bandeja de entrada

3. Haz click en el botón del email

---

## 📝 USUARIOS DE PRUEBA

Estos usuarios ya están creados (todos con password: `flash123`):

```
Username: admin
Email: admin@example.com

Username: juan  
Email: juan@example.com

Username: maria
Email: maria@example.com

Username: carlos
Email: carlos@example.com
```

---

## 🔒 SEGURIDAD

✅ **Implementado:**
- Tokens seguros con `default_token_generator`
- Validación de expiración (24 horas)
- UID codificado en base64
- No revela si el email existe (seguridad)
- Validación de fortaleza de contraseña
- Protección CSRF

⚠️ **Para producción:**
- Usa HTTPS siempre
- Configura `SECURE_SSL_REDIRECT = True`
- Usa variables de entorno para credenciales
- Nunca subas `.env` a Git (ya está en .gitignore)

---

## 🎨 CARACTERÍSTICAS DEL EMAIL

- ✅ Diseño responsive y profesional
- ✅ Gradiente morado/azul moderno
- ✅ Botón grande de acción
- ✅ Link alternativo si el botón no funciona
- ✅ Advertencia de seguridad
- ✅ Indicador de expiración (24h)
- ✅ Footer con branding
- ✅ Compatible con todos los clientes de email

---

## 🐛 TROUBLESHOOTING

**"SMTPAuthenticationError" al enviar con Gmail:**
- Verifica que la verificación en 2 pasos esté activa
- Usa una contraseña de aplicación (no tu contraseña normal de Gmail)
- Revisa que el email sea correcto en .env

**"No recibo el email en Gmail":**
- Revisa spam/correo no deseado
- Espera 1-2 minutos
- Verifica que el EMAIL_BACKEND esté en modo smtp

**"El link no funciona":**
- Verifica que no hayan pasado 24 horas
- Asegúrate de copiar el link completo
- No debe tener espacios o saltos de línea

---

## 💡 SIGUIENTES PASOS OPCIONALES

1. **Email de bienvenida** al registrarse
2. **Email de confirmación** de pedidos
3. **Notificaciones** de cambio de estado
4. **Alertas** de ofertas en wishlist
5. **Newsletter** para marketing

¿Quieres que implemente alguna de estas? 🚀
