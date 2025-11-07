# 🚀 INSTRUCCIONES PARA CONFIGURAR RENDER

## Variables de Entorno que DEBES agregar en Render

Ve a: **Dashboard de Render → flash-marketplace → Environment**

### 1. SENDGRID_API_KEY
```
SENDGRID_API_KEY=SG.dPssllyTr7tHaz_vsMog.KAj6QsF_tLKCSs-q8V_4IXKP2_0vyUYvbBTIcy_ZQe4
```

### 2. DEFAULT_FROM_EMAIL
```
DEFAULT_FROM_EMAIL=ivanandreshernandezc@gmail.com
```

### 3. EMAIL_BACKEND (si no está)
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

---

## ✅ Variables que YA DEBES TENER (verifica que estén correctas)

```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.dPssllyTr7tHaz_vsMog.KAj6QsF_tLKCSs-q8V_4IXKP2_0vyUYvbBTIcy_ZQe4
```

---

## 📝 PASOS PARA AGREGAR LAS VARIABLES:

1. Ve a https://dashboard.render.com
2. Haz clic en tu servicio **flash-marketplace**
3. Ve a la pestaña **Environment**
4. Haz clic en **"Add Environment Variable"**
5. Agrega cada variable (KEY y VALUE)
6. Haz clic en **"Save Changes"**
7. El servicio se reiniciará automáticamente (tarda 3-5 minutos)

---

## 🔍 DESPUÉS DE AGREGAR LAS VARIABLES:

1. Espera a que el deploy termine (verás "Live" en verde)
2. Ve a los **Logs** y verifica que no haya errores
3. Prueba la recuperación de contraseña en: https://flash-marketplace.onrender.com/cuenta/solicitar-recuperacion/

---

## ⚠️ IMPORTANTE:

- La API Key de SendGrid es la MISMA para `SENDGRID_API_KEY` y `EMAIL_HOST_PASSWORD`
- No uses comillas en los valores de las variables
- El email `ivanandreshernandezc@gmail.com` DEBE estar verificado en SendGrid
- Si cambias variables, Render reiniciará automáticamente el servicio
