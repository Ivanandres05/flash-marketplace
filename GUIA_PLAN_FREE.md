# 🚀 GUÍA SIMPLIFICADA - PARA PLAN FREE DE RENDER

## ✅ BUENAS NOTICIAS:
¡No necesitas Shell! He creado un comando automático que actualizará la base de datos durante el deploy.

---

## 🎯 SOLO 3 PASOS (8 MINUTOS TOTAL)

---

### 1️⃣ AGREGAR VARIABLES EN RENDER (2 minutos)

**URL:** https://dashboard.render.com

**Pasos:**
1. Selecciona tu servicio **flash-marketplace**
2. Clic en **"Environment"** (menú izquierdo)
3. Clic en **"Add Environment Variable"** 

**Agrega estas 3 variables (una por una):**

```
Variable 1:
KEY: SENDGRID_API_KEY
VALUE: SG.dPssllyTr7tHaz_vsMog.KAj6QsF_tLKCSs-q8V_4IXKP2_0vyUYvbBTIcy_ZQe4

Variable 2:
KEY: DEFAULT_FROM_EMAIL
VALUE: ivanandreshernandezc@gmail.com

Variable 3:
KEY: EMAIL_BACKEND
VALUE: django.core.mail.backends.smtp.EmailBackend
```

4. Después de agregar las 3, haz clic en **"Save Changes"**
5. Render comenzará a hacer deploy automáticamente

---

### 2️⃣ ESPERAR A QUE TERMINE EL DEPLOY (5 minutos)

**Qué verás:**
1. Status cambiará a **"Building..."** (1-2 min)
2. Luego **"Deploying..."** (2-3 min)
3. Finalmente **"Live"** ✅ (en verde)

**Mientras esperas, ve a los Logs:**
- Clic en **"Logs"** (menú superior)
- Busca estas líneas (confirman que todo funcionó):

```
✅ ACTUALIZANDO USUARIO IVAN EN BASE DE DATOS
✅ Email ACTUALIZADO a: ivanandreshernandezc@gmail.com
✅ Profile verificado
✅ ACTUALIZACIÓN COMPLETADA
```

**Si ves errores en rojo:**
- Copia el error completo
- Mándamelo para ayudarte

---

### 3️⃣ PROBAR RECUPERACIÓN DE CONTRASEÑA (1 minuto)

**Cuando veas "Live" en verde:**

1. **Ir a la página:**
   ```
   https://flash-marketplace.onrender.com/cuenta/solicitar-recuperacion/
   ```

2. **Ingresar tu email:**
   ```
   ivanandreshernandezc@gmail.com
   ```
   O también puedes usar tu username: `ivan`

3. **Clic en "Enviar Código"**

4. **Revisar tu Gmail:**
   - Inbox: busca "Flash Marketplace"
   - **También revisa SPAM** (muy importante)
   - Deberías ver un email con un código de 6 dígitos

5. **Si llega el email:**
   - ✅ Ingresa el código
   - ✅ Cambia tu contraseña
   - ✅ ¡FUNCIONÓ! 🎉

6. **Si NO llega:**
   - Espera 1-2 minutos más
   - Revisa bien la carpeta SPAM
   - Si aún no llega, mándame los logs de Render

---

## 📋 CHECKLIST RÁPIDO:

- [ ] ✅ Paso 1.1: Has agregado las 3 variables en Render
- [ ] ✅ Paso 1.2: Has dado clic en "Save Changes"
- [ ] ⏳ Paso 2.1: Render dice "Building..." o "Deploying..."
- [ ] ⏳ Paso 2.2: Esperando a que diga "Live"
- [ ] 🔍 Paso 2.3: Revisando logs (buscar "ACTUALIZACIÓN COMPLETADA")
- [ ] 🧪 Paso 3.1: Probando en la página
- [ ] 📧 Paso 3.2: Revisando Gmail (inbox + spam)
- [ ] 🎉 Paso 3.3: ¡Email recibido y funcionando!

---

## 🔧 QUÉ HACE EL SISTEMA AUTOMÁTICAMENTE:

### Durante el deploy, el sistema ejecutará:
1. ✅ Migraciones de base de datos
2. ✅ **Comando `fix_ivan_email`** (actualiza tu usuario automáticamente)
3. ✅ Recolección de archivos estáticos
4. ✅ Inicio del servidor

### El comando `fix_ivan_email` hace:
- Busca el usuario "ivan"
- Si existe: actualiza el email a `ivanandreshernandezc@gmail.com`
- Si no existe: lo crea con ese email
- Verifica que tenga Profile
- Todo aparece en los logs

---

## ⚡ CAMBIOS REALIZADOS:

### Nuevo archivo creado:
- `apps/accounts/management/commands/fix_ivan_email.py`
  - Comando Django que actualiza el usuario automáticamente
  - Se ejecuta en cada deploy (entre migrate y collectstatic)
  - Visible en los logs de Render

### Dockerfile actualizado:
- Agregada línea: `python manage.py fix_ivan_email`
- Se ejecuta después de migrate, antes de collectstatic

---

## 🆘 TROUBLESHOOTING:

### Problema: "No veo el comando fix_ivan_email en los logs"
**Solución:** El deploy anterior no incluyó el código. Espera a que termine este deploy.

### Problema: "Error: No module named sendgrid"
**Solución:** Verifica que `sendgrid==6.11.0` esté en requirements.txt (ya debe estar).

### Problema: Email no llega después de 5 minutos
**Solución:** 
1. Verifica que las 3 variables estén en Render
2. Revisa los logs, busca "ENVIANDO EMAIL CON SENDGRID API"
3. Mándame los logs completos

### Problema: "User matching query does not exist"
**Solución:** Usa el email completo: `ivanandreshernandezc@gmail.com` en lugar del username

---

## ⏱️ TIEMPO REAL:

- **Paso 1:** 2 minutos (agregar variables)
- **Paso 2:** 5 minutos (esperar deploy automático)
- **Paso 3:** 1 minuto (probar)
- **TOTAL:** ~8 minutos

---

## 🎯 EMPIEZA AHORA:

### TU ÚNICA TAREA:
1. Ve a Render
2. Agrega las 3 variables
3. Save Changes
4. Espera a que diga "Live"
5. Prueba la recuperación

**¡Eso es todo!** El resto es automático. 🚀

---

## 📝 NOTA:
Ya has completado el Paso 1 (agregaste las variables). 

**SIGUIENTE:** Solo espera a que Render termine de hacer deploy y verás en los logs que el usuario se actualiza automáticamente. Luego prueba en el Paso 3.

**Avísame cuando veas "Live" en Render** y probamos juntos. 💪
