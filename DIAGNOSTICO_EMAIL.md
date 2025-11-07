# 🔍 DIAGNÓSTICO COMPLETO - SISTEMA DE RECUPERACIÓN DE CONTRASEÑA

## 📊 ESTADO ACTUAL

### Base de Datos Local (SQLite)
```
Usuario: admin  | Email: admin@flashmarket.com
Usuario: arle   | Email: amorales18@cue.edu.co  
Usuario: ivan   | Email: ivanandreshernandezc@gmail.com
```

### Base de Datos Producción (Neon PostgreSQL)
⚠️ **DIFERENTE** - Los usuarios en producción tienen emails distintos
- **Usuario "ivan"** probablemente tiene: `hernandezcifuentesdiana2004@gmail.com`
- Esto explica por qué aparece ese email al intentar recuperar contraseña

---

## ❌ CAUSAS IDENTIFICADAS DEL PROBLEMA

### 1. ⚠️ **BASE DE DATOS DESINCRONIZADA** (CRÍTICO)
**Problema:** La base de datos local (SQLite) tiene usuarios diferentes a la de producción (Neon)

**Evidencia:**
- Local: usuario "ivan" tiene email `ivanandreshernandezc@gmail.com`
- Producción: usuario "ivan" tiene email `hernandezcifuentesdiana2004@gmail.com`

**Impacto:**
- Los correos se envían al email registrado en Neon
- Si ingresas "ivan", se busca en Neon y encuentra `hernandezcifuentesdiana2004@gmail.com`
- El código se envía a un email que puede no estar verificado en SendGrid

**Solución:**
```bash
# Opción A: Actualizar email en producción
python manage.py shell --settings=flash.settings.prod
from django.contrib.auth.models import User
user = User.objects.get(username='ivan')
user.email = 'ivanandreshernandezc@gmail.com'
user.save()
exit()

# Opción B: Crear nuevo usuario con email correcto
# Opción C: Usar el email alternativo (Profile.alternate_email)
```

---

### 2. 🔐 **SENDGRID - REMITENTES VERIFICADOS**
**Problema:** SendGrid solo permite enviar emails desde remitentes verificados

**Estado actual en SendGrid:**
✅ `ivanandreshernandezc@gmail.com` - VERIFICADO
✅ `hernandezcifuentesdiana2004@gmail.com` - VERIFICADO

**Configuración actual:**
```python
DEFAULT_FROM_EMAIL = 'ivanandreshernandezc@gmail.com'
```

**Impacto:** 
- ✅ El remitente está verificado, NO es causa del problema

---

### 3. 📧 **CONFIGURACIÓN SMTP EN RENDER**
**Estado actual:**
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net ✅
EMAIL_PORT=587 ✅
EMAIL_USE_TLS=True ✅
EMAIL_HOST_USER=apikey ✅
EMAIL_HOST_PASSWORD=SG.dPssllyTr7... ✅
```

**Falta agregar:**
```
SENDGRID_API_KEY=SG.dPssllyTr7tHaz_vsMog.KAj6QsF_tLKCSs-q8V_4IXKP2_0vyUYvbBTIcy_ZQe4
DEFAULT_FROM_EMAIL=ivanandreshernandezc@gmail.com
```

**Impacto:**
- Sin `SENDGRID_API_KEY`, `EMAIL_HOST_PASSWORD` podría quedarse vacío
- Sin `DEFAULT_FROM_EMAIL`, se usa el valor por defecto del código

---

### 4. ⏱️ **TIMEOUT EN PRODUCCIÓN**
**Problema:** Los logs de Render muestran `TimeoutError: timed out`

**Causas posibles:**
a) **Firewall de Render bloqueando puerto 587**
   - Render puede bloquear conexiones SMTP salientes
   - Solución: Usar SendGrid API en lugar de SMTP

b) **Thread no completa antes de respuesta**
   - El código usa threading para enviar emails
   - El thread tiene timeout de 5 segundos
   - En producción puede tardar más

c) **Conexión SMTP lenta desde Render**
   - La conexión a `smtp.sendgrid.net` desde servidores de Render puede ser lenta

**Evidencia en código:**
```python
email_thread.join(timeout=5.0)  # Solo espera 5 segundos
```

---

### 5. 🔄 **CÓDIGO USANDO SMTP EN LUGAR DE API**
**Problema:** El código actual usa SMTP (puerto 587) en lugar de la API de SendGrid

**Desventaja de SMTP:**
- Más lento
- Más propenso a timeouts
- Requiere puerto 587 abierto
- Menos confiable en producción

**Ventaja de usar SendGrid API:**
- Más rápido (HTTP REST)
- Sin problemas de puertos
- Más confiable
- Mejor manejo de errores

**Código actual (SMTP):**
```python
server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
server.starttls()
server.login(smtp_user, smtp_password)
server.send_message(msg)
```

**Alternativa con API:**
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
message = Mail(...)
response = sg.send(message)
```

---

### 6. 🛡️ **CONFIGURACIÓN DE PRODUCCIÓN**
**Archivo:** `flash/settings/prod.py`

**Posible problema:**
```python
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
```

**Si `EMAIL_BACKEND` no está en Render:**
- Se usa `console.EmailBackend` (solo imprime en consola, no envía)
- Los emails NO se envían realmente

**Verificar en Render:**
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

---

## 🎯 SOLUCIONES PRIORITARIAS

### Solución 1: AGREGAR VARIABLES FALTANTES EN RENDER (Urgente)
```
SENDGRID_API_KEY=SG.dPssllyTr7tHaz_vsMog.KAj6QsF_tLKCSs-q8V_4IXKP2_0vyUYvbBTIcy_ZQe4
DEFAULT_FROM_EMAIL=ivanandreshernandezc@gmail.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

### Solución 2: SINCRONIZAR BASE DE DATOS (Crítico)
Actualizar el email del usuario "ivan" en Neon a `ivanandreshernandezc@gmail.com`

### Solución 3: MIGRAR DE SMTP A SENDGRID API (Recomendado)
Cambiar la implementación de envío de emails para usar la API REST de SendGrid

### Solución 4: AUMENTAR TIMEOUT DEL THREAD
Cambiar de 5 segundos a 15-30 segundos:
```python
email_thread.join(timeout=30.0)  # Aumentar timeout
```

### Solución 5: REMOVER THREADING (Más Simple)
Enviar el email de forma síncrona usando `send_mail()` de Django:
```python
send_mail(
    subject='Código de Recuperación',
    message=message,
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[destination_email],
    fail_silently=False,
)
```

---

## 📝 ORDEN DE IMPLEMENTACIÓN RECOMENDADO

1. **INMEDIATO:** Agregar variables `SENDGRID_API_KEY` y `DEFAULT_FROM_EMAIL` en Render
2. **IMPORTANTE:** Verificar/actualizar email del usuario "ivan" en Neon
3. **PRUEBA:** Intentar recuperar contraseña nuevamente
4. **SI FALLA:** Migrar a SendGrid API (solución más robusta)
5. **ALTERNATIVA:** Remover threading y usar `send_mail()` directo

---

## 🧪 CÓMO VERIFICAR CADA CAUSA

### Verificar email en Neon:
```bash
# Conectarse a Neon y ejecutar:
SELECT username, email FROM auth_user WHERE username = 'ivan';
```

### Verificar variables en Render:
Dashboard → Environment → Buscar "EMAIL" y "SENDGRID"

### Verificar logs de Render:
Dashboard → Logs → Buscar "DIAGNÓSTICO SMTP" o "ERROR"

### Probar envío manual:
```python
# En shell de Django (producción)
from django.core.mail import send_mail
send_mail(
    'Test',
    'Mensaje de prueba',
    'ivanandreshernandezc@gmail.com',
    ['ivanandreshernandezc@gmail.com'],
    fail_silently=False,
)
```

---

## ⚡ PRÓXIMOS PASOS SUGERIDOS

¿Qué quieres hacer primero?

A) Agregar las variables faltantes en Render y probar
B) Verificar/corregir el email del usuario "ivan" en Neon
C) Migrar a SendGrid API (solución más robusta)
D) Simplificar código removiendo threading
