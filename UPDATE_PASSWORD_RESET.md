# 🚀 Actualización - Sistema de Recuperación de Contraseña

## ✅ Cambios Realizados

### 1. **Nuevo Modelo**
- ✅ `PasswordResetCode` - Códigos de 6 dígitos con expiración de 15 minutos

### 2. **Nuevas Vistas**
- ✅ `request_password_reset` - Solicitar código por email
- ✅ `verify_reset_code` - Verificar código de 6 dígitos
- ✅ `reset_password` - Cambiar contraseña

### 3. **Nuevas URLs**
- ✅ `/cuenta/solicitar-recuperacion/` 
- ✅ `/cuenta/verificar-codigo/`
- ✅ `/cuenta/restablecer-contrasena/`

### 4. **Templates**
- ✅ `request_password_reset.html`
- ✅ `verify_reset_code.html`
- ✅ `reset_password.html`

### 5. **Configuración Email**
- ✅ SMTP configurado en `settings/base.py`
- ✅ Variables de entorno documentadas en `.env.example`

---

## 📋 Para Hacer Deploy

### Paso 1: Commit y Push
```bash
git add .
git commit -m "Añadir sistema de recuperación de contraseña con código por email"
git push origin main
```

### Paso 2: Ejecutar Migración en Render

En el **Shell de Render**:
```bash
python manage.py migrate accounts
```

### Paso 3: Configurar Variables de Entorno en Render

En **Render Dashboard → Environment**:

**Opción A: Gmail (Recomendado para testing)**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion
```

**Cómo obtener Password de Aplicación de Gmail:**
1. Ir a: https://myaccount.google.com/apppasswords
2. Crear nueva contraseña de aplicación
3. Copiar el código de 16 caracteres
4. Pegar en `EMAIL_HOST_PASSWORD`

**Opción B: SendGrid (Recomendado para producción)**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu-api-key-de-sendgrid
```

**Opción C: Console (Solo para testing - emails en logs)**
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Paso 4: Redeploy

Render hará **auto-deploy** cuando hagas push a `main`.

Si no, en Render Dashboard:
- Click en "Manual Deploy" → "Deploy latest commit"

---

## 🧪 Probar Localmente (Opcional)

```bash
# 1. Aplicar migración
python manage.py migrate

# 2. Configurar email en .env (opcional)
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-app

# 3. Ejecutar servidor
python manage.py runserver 8080

# 4. Probar en: http://localhost:8080/cuenta/solicitar-recuperacion/
```

---

## 📧 Flujo de Usuario

1. **Usuario olvida contraseña** → Click en "¿Olvidaste tu contraseña?" en login
2. **Ingresa email** → Recibe código de 6 dígitos
3. **Ingresa código** → Verifica código (válido 15 min)
4. **Nueva contraseña** → Cambia contraseña exitosamente
5. **Login** → Puede iniciar sesión con nueva contraseña

---

## 🔒 Seguridad Implementada

- ✅ Códigos de 6 dígitos aleatorios
- ✅ Expiración automática en 15 minutos
- ✅ Un solo uso por código
- ✅ Invalidación de códigos anteriores
- ✅ No revela si el email existe en el sistema
- ✅ Validación de longitud mínima de contraseña (8 caracteres)

---

## 📊 Tabla de Códigos en Admin

Puedes ver los códigos generados en:
- Django Admin → Accounts → Password Reset Codes

---

## ⚠️ Importante

1. **No subas credenciales de email a GitHub**
   - `.env` debe estar en `.gitignore` ✅
   - Configura variables en Render Dashboard

2. **Gmail puede bloquear "apps menos seguras"**
   - Usa contraseñas de aplicación
   - O mejor usa SendGrid/Mailgun para producción

3. **Límites de Gmail**
   - 500 emails/día (free)
   - Para producción real: SendGrid, AWS SES, Mailgun

---

## 🎯 Comandos Rápidos

```bash
# Commit y push
git add . && git commit -m "Sistema de recuperación de contraseña" && git push

# En Shell de Render (después del deploy)
python manage.py migrate accounts
```

---

## ✅ Checklist Final

- [ ] Commit y push a GitHub
- [ ] Esperar auto-deploy de Render (o hacer manual deploy)
- [ ] Ejecutar `python manage.py migrate accounts` en Shell de Render
- [ ] Configurar variables EMAIL_* en Render Environment
- [ ] Probar flujo completo en producción:
  - [ ] Solicitar código
  - [ ] Verificar email recibido
  - [ ] Ingresar código
  - [ ] Cambiar contraseña
  - [ ] Login con nueva contraseña

---

¡Listo para deploy! 🚀
