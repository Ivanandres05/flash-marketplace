# ⚡ Flash Marketplace - Resumen de Despliegue

## 🎯 Archivos Creados/Actualizados

### ✅ Archivos Docker
- `Dockerfile` - Configuración de contenedor con Python 3.13.7 + Gunicorn
- `docker-compose.yml` - Orquestación para desarrollo local
- `.dockerignore` - Archivos excluidos del build

### ✅ Configuración de Base de Datos
- `flash/settings/prod.py` - Actualizado con dj-database-url para Neon PostgreSQL
- `migrate_to_neon.sh` - Script para migrar datos de SQLite a Neon

### ✅ Variables de Entorno
- `.env.example` - Template de variables necesarias
- `render.yaml` - Configuración automática para Render

### ✅ Dependencias Actualizadas
- `requirements.txt` - Agregado:
  - `dj-database-url==2.1.0` (para Neon PostgreSQL)
  - `gunicorn==21.2.0` (servidor WSGI producción)
  - `whitenoise==6.6.0` (archivos estáticos)

### ✅ Documentación
- `DEPLOY_GUIDE.md` - Guía completa paso a paso

---

## 🚀 Pasos Rápidos para Desplegar

### 1️⃣ Configurar Neon PostgreSQL (5 minutos)
```bash
# 1. Crear cuenta en https://neon.tech
# 2. Crear proyecto "flash-marketplace"
# 3. Copiar DATABASE_URL (incluye ?sslmode=require)
```

### 2️⃣ Migrar Datos (10 minutos)
```bash
# Exportar desde SQLite
python manage.py dumpdata --natural-foreign --natural-primary \
  --exclude contenttypes --exclude auth.permission \
  --indent 2 > data_backup.json

# Configurar .env con DATABASE_URL de Neon
echo "DATABASE_URL=postgresql://..." > .env
echo "DJANGO_SETTINGS_MODULE=flash.settings.prod" >> .env

# Migrar estructura
python manage.py migrate

# Cargar datos
python manage.py loaddata data_backup.json
```

### 3️⃣ Subir a GitHub (3 minutos)
```bash
git init
git add .
git commit -m "Preparar para despliegue en Render con Neon"
git remote add origin https://github.com/TU_USUARIO/flash-marketplace.git
git push -u origin main
```

### 4️⃣ Desplegar en Render (10 minutos)
```bash
# 1. Ir a https://render.com → New + → Web Service
# 2. Conectar repositorio GitHub
# 3. Configurar:
#    - Runtime: Docker
#    - Branch: main
#    - Instance: Free

# 4. Variables de entorno:
DJANGO_SECRET_KEY=<generar-con-comando-abajo>
DEBUG=False
DJANGO_SETTINGS_MODULE=flash.settings.prod
DATABASE_URL=<copiar-de-neon>
ALLOWED_HOSTS=tu-app.onrender.com

# 5. Deploy automático
```

### 5️⃣ Generar SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## ✅ Checklist Final

- [ ] Neon PostgreSQL creado
- [ ] DATABASE_URL obtenido (con ?sslmode=require)
- [ ] Datos migrados de SQLite a Neon
- [ ] Repositorio en GitHub actualizado
- [ ] Render configurado con variables de entorno
- [ ] Primer despliegue exitoso
- [ ] Migraciones ejecutadas en producción
- [ ] Superusuario creado
- [ ] Sitio accesible en https://tu-app.onrender.com
- [ ] Admin panel funcionando (/admin/)
- [ ] Archivos estáticos cargando correctamente

---

## 🐛 Comandos de Diagnóstico

### Ver logs en Render
```
Dashboard → Tu servicio → Logs
```

### Shell en Render
```bash
# Dashboard → Shell
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Probar localmente con Docker
```bash
docker-compose up --build
# Acceder a: http://localhost:8000
```

---

## 📊 Arquitectura Final

```
┌─────────────────┐
│   Render.com    │  ← Tu backend Django (Docker + Gunicorn)
│  Web Service    │     Puerto 8000, HTTPS automático
└────────┬────────┘
         │
         ├── Static Files (WhiteNoise)
         │
         └── Database
             │
             ▼
     ┌───────────────┐
     │  Neon (PG)    │  ← PostgreSQL serverless
     │   Database    │     Backups automáticos
     └───────────────┘
```

---

## 🎓 Próximos Pasos Recomendados

1. **Monitoreo**: Configurar Sentry para rastrear errores
2. **CDN**: Usar Cloudflare para acelerar contenido estático
3. **Email**: Configurar SendGrid/Mailgun para emails transaccionales
4. **Storage**: Migrar archivos media a AWS S3/Cloudinary
5. **Cache**: Agregar Redis para mejorar rendimiento
6. **CI/CD**: Configurar GitHub Actions para tests automáticos

---

## 📞 Soporte

- **Render Docs**: https://render.com/docs
- **Neon Docs**: https://neon.tech/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.1/howto/deployment/

---

**Tiempo estimado total: 30-45 minutos** ⏱️

¡Tu proyecto estará en producción! 🎉
