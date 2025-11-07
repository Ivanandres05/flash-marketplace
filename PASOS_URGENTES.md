# ✅ PASOS QUE DEBES HACER AHORA MISMO

## 🎯 PASO 1: AGREGAR VARIABLES EN RENDER (URGENTE - 5 minutos)

1. **Abre Render Dashboard:**
   - Ve a: https://dashboard.render.com
   - Haz clic en **flash-marketplace**

2. **Ve a la pestaña Environment:**
   - Haz clic en **"Environment"** en el menú izquierdo

3. **Agrega estas 3 variables** (haz clic en "Add Environment Variable" para cada una):

   **Variable 1:**
   ```
   KEY: SENDGRID_API_KEY
   VALUE: SG.dPssllyTr7tHaz_vsMog.KAj6QsF_tLKCSs-q8V_4IXKP2_0vyUYvbBTIcy_ZQe4
   ```

   **Variable 2:**
   ```
   KEY: DEFAULT_FROM_EMAIL
   VALUE: ivanandreshernandezc@gmail.com
   ```

   **Variable 3** (si no existe):
   ```
   KEY: EMAIL_BACKEND
   VALUE: django.core.mail.backends.smtp.EmailBackend
   ```

4. **Guarda los cambios:**
   - Haz clic en **"Save Changes"**
   - El servicio se reiniciará automáticamente (tarda 3-5 minutos)
   - Verás que el status cambia a "Building" y luego "Deploying"

5. **Espera a que termine:**
   - Cuando veas "Live" en verde, el deploy está completo

---

## 🔍 PASO 2: VERIFICAR USUARIO EN NEON (OPCIONAL pero recomendado)

Para verificar qué email tiene el usuario "ivan" en la base de datos de producción:

1. **Opción A: Usar Neon Dashboard**
   - Ve a: https://console.neon.tech
   - Selecciona tu proyecto
   - Ve a "SQL Editor"
   - Ejecuta: `SELECT username, email FROM auth_user WHERE username = 'ivan';`

2. **Opción B: Usar el script que creé**
   ```bash
   # Necesitas tener las credenciales de Neon configuradas
   python check_neon_user.py
   ```

**Si el email es incorrecto**, el script te permitirá actualizarlo a `ivanandreshernandezc@gmail.com`

---

## ✅ PASO 3: PROBAR LA RECUPERACIÓN (Después de que Render termine)

1. Ve a: https://flash-marketplace.onrender.com/cuenta/solicitar-recuperacion/

2. Ingresa el email o username: **ivan** o **ivanandreshernandezc@gmail.com**

3. Haz clic en "Enviar código"

4. **Revisa tu bandeja de entrada** en `ivanandreshernandezc@gmail.com`
   - También revisa la carpeta de SPAM

5. Si llega el email:
   - ✅ ¡TODO FUNCIONA!
   - Ingresa el código de 6 dígitos
   - Cambia tu contraseña

6. Si NO llega el email:
   - Ve a Render → Logs
   - Busca mensajes que digan "ENVIANDO EMAIL CON SENDGRID API"
   - Copia los logs y pégamelos para diagnosticar

---

## 📊 QUÉ CAMBIÓ:

### ✅ Código actualizado (ya está en GitHub y Render se actualizará):
- **Migración de SMTP a SendGrid API:** Mucho más confiable, sin problemas de puertos
- **Emails HTML formateados:** Ahora los emails se ven profesionales
- **Mejor manejo de errores:** Mensajes más claros en los logs
- **Fallback a send_mail:** Si SendGrid falla, intenta con el método de Django

### ⏳ Lo que FALTA (debes hacerlo TÚ):
- ❌ Agregar las 3 variables en Render (CRÍTICO)
- ⚠️ Verificar/corregir email del usuario "ivan" en Neon (recomendado)

---

## 🆘 SI ALGO FALLA:

### Problema 1: "SENDGRID_API_KEY no configurado"
**Solución:** Verifica que agregaste la variable en Render correctamente

### Problema 2: "Usuario 'ivan' no encontrado"
**Solución:** Usa el email completo: `ivanandreshernandezc@gmail.com`

### Problema 3: Email llega pero al correo equivocado
**Solución:** El usuario en Neon tiene un email diferente. Actualízalo con el script o en Neon Dashboard

### Problema 4: No llega ningún email
**Solución:** 
1. Verifica que las 3 variables estén en Render
2. Revisa los logs de Render
3. Verifica que `ivanandreshernandezc@gmail.com` esté verificado en SendGrid

---

## 📋 CHECKLIST RÁPIDO:

- [ ] Agregar `SENDGRID_API_KEY` en Render
- [ ] Agregar `DEFAULT_FROM_EMAIL` en Render  
- [ ] Agregar `EMAIL_BACKEND` en Render
- [ ] Guardar cambios en Render
- [ ] Esperar a que el deploy termine (status "Live")
- [ ] Probar recuperación en https://flash-marketplace.onrender.com/cuenta/solicitar-recuperacion/
- [ ] Revisar inbox de ivanandreshernandezc@gmail.com
- [ ] Si no llega, revisar logs en Render y reportarme

---

## ⚡ TIEMPO ESTIMADO:
- Agregar variables en Render: **2 minutos**
- Esperar deploy: **3-5 minutos**
- Probar: **1 minuto**
- **TOTAL: ~10 minutos**

---

¡Empieza con el PASO 1 AHORA! Una vez que agregues las variables, avísame y verificamos juntos. 🚀
