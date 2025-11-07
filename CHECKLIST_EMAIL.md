# ✅ Checklist de Variables de Entorno en Render

## Variables CRÍTICAS que DEBES tener en Render:

Ve a: **Render Dashboard → flash-marketplace → Environment**

### 1. EMAIL_BACKEND (MÁS IMPORTANTE)
```
Nombre: EMAIL_BACKEND
Valor: django.core.mail.backends.smtp.EmailBackend
```
⚠️ **DEBE ser `smtp.EmailBackend`** NO `console.EmailBackend`

### 2. EMAIL_HOST
```
Nombre: EMAIL_HOST
Valor: smtp.gmail.com
```

### 3. EMAIL_PORT
```
Nombre: EMAIL_PORT
Valor: 587
```

### 4. EMAIL_USE_TLS
```
Nombre: EMAIL_USE_TLS
Valor: True
```

### 5. EMAIL_HOST_USER
```
Nombre: EMAIL_HOST_USER
Valor: ivanandreshernandezc@gmail.com
```

### 6. EMAIL_HOST_PASSWORD
```
Nombre: EMAIL_HOST_PASSWORD
Valor: yfwdvfuwqmpgkrdv
```

---

## 🔍 Cómo verificar en Render:

1. Ve a https://dashboard.render.com
2. Selecciona "flash-marketplace"
3. Clic en pestaña "Environment"
4. Busca cada variable en la lista
5. Si falta alguna, clic en "Add Environment Variable"
6. Guarda los cambios (esto hará un nuevo deploy)

---

## 🚨 Si ya las agregaste pero sigue sin funcionar:

### Ver los logs en tiempo real:
1. Render Dashboard → flash-marketplace
2. Pestaña "Logs"
3. Intenta solicitar código de recuperación
4. Busca en logs mensajes como:
   - ✓ "Email enviado a..."
   - ✗ "Error al enviar email..."

---

## 🧪 Probar localmente (FUNCIONA):

```bash
cd C:/Users/ivana/OneDrive/Desktop/Flash

export EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
export EMAIL_HOST="smtp.gmail.com"
export EMAIL_PORT="587"
export EMAIL_USE_TLS="True"
export EMAIL_HOST_USER="ivanandreshernandezc@gmail.com"
export EMAIL_HOST_PASSWORD="yfwdvfuwqmpgkrdv"

python test_email.py
```

Esto debería enviar un email de prueba exitosamente.

---

## ✅ Estado actual:

- ✅ Código corregido (threading fix)
- ✅ Deploy exitoso
- ✅ Variables configuradas (según screenshot)
- ⏳ **FALTA PROBAR** en producción

**Próximo paso:** Intenta solicitar código de recuperación y mira si llega el email.
