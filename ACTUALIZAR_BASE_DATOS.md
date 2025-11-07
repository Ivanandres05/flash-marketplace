# 🗄️ GUÍA COMPLETA: ACTUALIZAR BASE DE DATOS EN NEON

## 🎯 OBJETIVO:
Asegurar que el usuario "ivan" en Neon tenga el email correcto: `ivanandreshernandezc@gmail.com`

---

## 📋 OPCIÓN 1: USAR RENDER SHELL (MÁS RÁPIDO - 2 minutos)

### Paso 1: Abrir Render Shell
1. Ve a: https://dashboard.render.com/web/srv-d46aekemcj7s73bedmr0
2. Haz clic en **"Shell"** en el menú superior
3. Espera a que se conecte (aparecerá `~ $`)

### Paso 2: Ejecutar comandos Django
Copia y pega estos comandos uno por uno:

```bash
# 1. Abrir Django shell
python manage.py shell --settings=flash.settings.prod
```

Luego dentro del shell de Python, copia y pega TODO esto:

```python
from django.contrib.auth.models import User
from apps.accounts.models import Profile

# Buscar o crear usuario ivan
ivan, created = User.objects.get_or_create(
    username='ivan',
    defaults={
        'email': 'ivanandreshernandezc@gmail.com',
        'first_name': 'Ivan',
        'last_name': 'Hernandez'
    }
)

if created:
    ivan.set_password('FlashMarket2025!')
    ivan.save()
    print('✅ Usuario ivan CREADO')
else:
    # Actualizar email si es diferente
    if ivan.email != 'ivanandreshernandezc@gmail.com':
        print(f'⚠️ Email anterior: {ivan.email}')
        ivan.email = 'ivanandreshernandezc@gmail.com'
        ivan.save()
        print('✅ Email ACTUALIZADO')
    else:
        print('✅ Email ya correcto')

# Asegurar profile
profile, created = Profile.objects.get_or_create(user=ivan)

print(f'\n📊 Usuario ivan:')
print(f'   Username: {ivan.username}')
print(f'   Email: {ivan.email}')
print(f'   Nombre: {ivan.first_name} {ivan.last_name}')

# Salir
exit()
```

---

## 📋 OPCIÓN 2: USAR NEON SQL EDITOR (DIRECTO - 1 minuto)

### Paso 1: Abrir Neon Console
1. Ve a: https://console.neon.tech
2. Selecciona tu proyecto
3. Haz clic en **"SQL Editor"**

### Paso 2: Verificar usuario actual
```sql
SELECT id, username, email, first_name, last_name 
FROM auth_user 
WHERE username = 'ivan';
```

### Paso 3a: Si el usuario existe, actualizar email
```sql
UPDATE auth_user 
SET email = 'ivanandreshernandezc@gmail.com',
    first_name = 'Ivan',
    last_name = 'Hernandez'
WHERE username = 'ivan';
```

### Paso 3b: Si el usuario NO existe, crearlo
```sql
-- Primero necesitas obtener el hash de la contraseña
-- Es más fácil usar Render Shell para esto
```

---

## 📋 OPCIÓN 3: EJECUTAR SCRIPT DESDE LOCAL (Avanzado)

### Prerequisitos:
- Tener configurado DATABASE_URL de Neon en tu .env local

### Comando:
```bash
cd "/c/Users/ivana/OneDrive/Desktop/Flash"
python update_neon_database.py
```

---

## ✅ VERIFICAR QUE FUNCIONÓ:

Después de actualizar, verifica en Render Shell:

```bash
python manage.py shell --settings=flash.settings.prod
```

```python
from django.contrib.auth.models import User
ivan = User.objects.get(username='ivan')
print(f'Email: {ivan.email}')
exit()
```

Deberías ver: `Email: ivanandreshernandezc@gmail.com`

---

## 🚀 ORDEN RECOMENDADO DE ACCIONES:

1. **PRIMERO:** Agregar variables en Render (SENDGRID_API_KEY, etc.)
2. **SEGUNDO:** Actualizar base de datos usando Render Shell (Opción 1)
3. **TERCERO:** Hacer Manual Redeploy en Render
4. **CUARTO:** Probar recuperación de contraseña

---

## ⚡ RESUMEN RÁPIDO - COMANDOS PARA COPIAR Y PEGAR:

### En Render Shell:
```bash
python manage.py shell --settings=flash.settings.prod
```

### Luego en Python:
```python
from django.contrib.auth.models import User
from apps.accounts.models import Profile

ivan, created = User.objects.get_or_create(username='ivan', defaults={'email': 'ivanandreshernandezc@gmail.com', 'first_name': 'Ivan', 'last_name': 'Hernandez'})

if not created and ivan.email != 'ivanandreshernandezc@gmail.com':
    ivan.email = 'ivanandreshernandezc@gmail.com'
    ivan.save()
    print('✅ Email actualizado')
else:
    print('✅ Email correcto')

Profile.objects.get_or_create(user=ivan)
print(f'Usuario: {ivan.username} | Email: {ivan.email}')
exit()
```

---

## 📝 NOTA IMPORTANTE:

Si el usuario "ivan" NO existe en Neon, el script lo creará con:
- Username: `ivan`
- Email: `ivanandreshernandezc@gmail.com`
- Password: `FlashMarket2025!` (cámbiala después de iniciar sesión)

---

¿Listo? Empieza con la **OPCIÓN 1 (Render Shell)** - es la más rápida y confiable. 🚀
