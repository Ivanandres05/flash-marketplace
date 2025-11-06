# Flash Marketplace - Guía de Despliegue

Esta guía te llevará paso a paso para desplegar Flash Marketplace usando Docker, Neon PostgreSQL y Render.

---

## 📋 Pre-requisitos

- [ ] Git instalado
- [ ] Docker instalado
- [ ] Cuenta en GitHub
- [ ] Cuenta en Neon (https://neon.tech)
- [ ] Cuenta en Render (https://render.com)

---

## 🗄️ PASO 1: Migrar a Neon PostgreSQL

### 1.1 Crear base de datos en Neon

1. Ve a https://console.neon.tech
2. Click en "Create a project"
3. Nombre: `flash-marketplace`
4. Copia la **Connection String** (DATABASE_URL)
   - Formato: `postgresql://user:password@host.neon.tech/dbname?sslmode=require`

### 1.2 Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

Edita `.env` y configura:

```env
DEBUG=False
SECRET_KEY=genera-una-clave-secreta-aqui
DJANGO_SETTINGS_MODULE=flash.settings.prod
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com
SITE_URL=https://tu-app.onrender.com
```

### 1.3 Migrar datos de SQLite a Neon

**Opción A: Usar script Python (Windows/Linux/Mac)**

```bash
python migrate_to_neon.py
```

**Opción B: Comandos manuales**

```bash
# 1. Exportar datos desde SQLite
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --exclude auth.permission \
    --exclude contenttypes \
    --exclude admin.logentry \
    --exclude sessions.session \
    --indent 2 > backup_data.json

# 2. Crear tablas en Neon
python manage.py migrate --settings=flash.settings.prod

# 3. Importar datos a Neon
python manage.py loaddata backup_data.json --settings=flash.settings.prod
```

### 1.4 Verificar migración

```bash
python manage.py shell --settings=flash.settings.prod
```

En el shell de Python:
```python
from django.contrib.auth.models import User
print(f"Usuarios: {User.objects.count()}")
from apps.catalog.models import Product
print(f"Productos: {Product.objects.count()}")
```

---

## 🐳 PASO 2: Probar con Docker localmente

### 2.1 Construir imagen Docker

```bash
docker build -t flash-marketplace .
```

### 2.2 Ejecutar con docker-compose

```bash
docker-compose up
```

Accede a http://localhost:8000

### 2.3 Detener contenedores

```bash
docker-compose down
```

---

## 📦 PASO 3: Subir a GitHub

### 3.1 Inicializar repositorio (si no existe)

```bash
git init
git add .
git commit -m "Configuración inicial para despliegue"
```

### 3.2 Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `flash-marketplace`
3. **NO** inicialices con README, .gitignore o licencia

### 3.3 Conectar y subir

```bash
git remote add origin https://github.com/TU-USUARIO/flash-marketplace.git
git branch -M main
git push -u origin main
```

**IMPORTANTE:** Asegúrate de que `.env` esté en `.gitignore` y NO se suba a GitHub.

---

## 🚀 PASO 4: Desplegar en Render

### 4.1 Crear Web Service en Render

1. Ve a https://dashboard.render.com
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub: `flash-marketplace`

### 4.2 Configurar el Web Service

**Configuración básica:**
- **Name:** `flash-marketplace`
- **Region:** Oregon (US West) o el más cercano
- **Branch:** `main`
- **Root Directory:** (dejar vacío)
- **Environment:** `Docker`
- **Instance Type:** `Free` (para empezar)

**Render detectará automáticamente el Dockerfile**

### 4.3 Configurar Variables de Entorno

En "Environment" → "Environment Variables", agrega:

```
DEBUG=False
SECRET_KEY=tu-secret-key-super-segura-cambiar-aqui
DJANGO_SETTINGS_MODULE=flash.settings.prod
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
ALLOWED_HOSTS=.onrender.com
SITE_URL=https://flash-marketplace.onrender.com
STATIC_ROOT=/app/staticfiles
MEDIA_ROOT=/app/media
```

### 4.4 Desplegar

1. Click en "Create Web Service"
2. Render automáticamente:
   - Clonará tu repositorio
   - Construirá la imagen Docker
   - Ejecutará el contenedor
   - Asignará una URL: `https://flash-marketplace.onrender.com`

### 4.5 Ejecutar migraciones (primera vez)

Después del primer despliegue, ve a "Shell" en Render y ejecuta:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## ✅ PASO 5: Verificar el despliegue

### 5.1 Probar la aplicación

1. Accede a: `https://tu-app.onrender.com`
2. Prueba el login: `https://tu-app.onrender.com/cuenta/login/`
3. Accede al admin: `https://tu-app.onrender.com/admin/`

### 5.2 Verificar archivos estáticos

- Los archivos estáticos deberían cargarse correctamente gracias a WhiteNoise
- Si hay problemas, ejecuta en Render Shell:
  ```bash
  python manage.py collectstatic --noinput
  ```

### 5.3 Verificar base de datos

En Render Shell:
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
print(User.objects.count())
```

---

## 🔧 Comandos útiles en Render

### Acceder al shell del contenedor
En el dashboard de Render → "Shell"

### Ver logs
En el dashboard de Render → "Logs"

### Reiniciar el servicio
En el dashboard de Render → "Manual Deploy" → "Deploy latest commit"

### Ejecutar comandos Django
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py shell
```

---

## 📊 Arquitectura del despliegue

```
┌─────────────────┐
│   GitHub Repo   │
│  (código fuente)│
└────────┬────────┘
         │
         │ git push
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   Render.com    │◄────►│ Neon PostgreSQL  │
│  (Docker + Web) │      │   (Base de datos)│
│                 │      │                  │
│ - Gunicorn      │      │ - 7 usuarios     │
│ - WhiteNoise    │      │ - Productos      │
│ - Django 5.2.7  │      │ - Pedidos        │
└─────────────────┘      └──────────────────┘
         │
         │ HTTPS
         ▼
    ┌─────────┐
    │ Usuarios│
    └─────────┘
```

---

## 🐛 Troubleshooting

### Error: "Application failed to respond"
- Verifica que Gunicorn esté en requirements.txt
- Revisa logs en Render
- Verifica que el puerto sea 8000

### Error: "Static files not found"
```bash
python manage.py collectstatic --noinput
```

### Error: "Database connection failed"
- Verifica DATABASE_URL en Render
- Asegúrate de incluir `?sslmode=require`
- Verifica que Neon esté activo

### Error: "Bad Request (400)"
- Agrega tu dominio de Render a ALLOWED_HOSTS
- Formato: `.onrender.com`

---

## 🔒 Seguridad en producción

✅ **Implementado:**
- DEBUG=False
- SECRET_KEY desde variable de entorno
- HTTPS obligatorio (SECURE_SSL_REDIRECT)
- Cookies seguras
- XSS Protection
- HSTS Headers
- WhiteNoise para servir estáticos de forma segura

❌ **NO hacer:**
- Subir `.env` a GitHub
- Usar DEBUG=True en producción
- Exponer SECRET_KEY
- Usar contraseñas débiles

---

## 📝 Notas adicionales

### Archivos importantes creados:
- `Dockerfile` - Configuración del contenedor
- `docker-compose.yml` - Orquestación local
- `.env.example` - Template de variables de entorno
- `flash/settings/prod.py` - Configuración de producción actualizada
- `migrate_to_neon.py` - Script de migración a PostgreSQL
- `requirements.txt` - Actualizado con dependencias de producción

### Flujo de trabajo recomendado:
1. Desarrolla localmente con SQLite (settings.dev)
2. Prueba con Docker + Neon localmente (settings.prod)
3. Haz commit y push a GitHub
4. Render desplegará automáticamente

### Costos estimados:
- **Neon (PostgreSQL):** Free tier (hasta 500 MB, suficiente para empezar)
- **Render (Web Service):** Free tier (con limitaciones, $7/mes para instancia estable)
- **Total mínimo:** $0/mes (free tiers) o $7/mes (con instancia pagada)

---

## 🎉 ¡Listo!

Tu aplicación Flash Marketplace ahora está en producción con:
- ✅ Base de datos PostgreSQL en la nube (Neon)
- ✅ Aplicación contenerizada (Docker)
- ✅ Desplegada en Render con HTTPS
- ✅ Archivos estáticos servidos eficientemente (WhiteNoise)
- ✅ Configuración segura para producción

**URL de tu aplicación:** https://tu-app.onrender.com

---

## 📚 Recursos

- [Documentación de Render](https://render.com/docs)
- [Documentación de Neon](https://neon.tech/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
