# 🚀 Guía de Despliegue: Flash Marketplace

## 📦 PARTE 1: Configuración de Neon PostgreSQL

### 1.1 Crear cuenta en Neon
1. Ve a https://neon.tech
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto: "flash-marketplace"

### 1.2 Obtener DATABASE_URL
1. En tu proyecto Neon, ve a "Dashboard"
2. Copia la cadena de conexión (Connection String)
3. Debe verse así:
   ```
   postgresql://usuario:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
   ```

### 1.3 Migrar datos desde SQLite

#### Opción A: Usando el script (Linux/Mac/Git Bash)
```bash
chmod +x migrate_to_neon.sh
./migrate_to_neon.sh
```

#### Opción B: Manual (Windows/Todos)
```bash
# 1. Exportar datos de SQLite
python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --exclude admin.logentry --indent 2 > data_backup.json

# 2. Crear archivo .env con DATABASE_URL de Neon
echo "DATABASE_URL=postgresql://..." > .env
echo "DJANGO_SETTINGS_MODULE=flash.settings.prod" >> .env
echo "DEBUG=False" >> .env

# 3. Ejecutar migraciones en Neon
python manage.py migrate

# 4. Cargar datos en Neon
python manage.py loaddata data_backup.json

# 5. Crear superusuario si es necesario
python manage.py createsuperuser
```

---

## 🐳 PARTE 2: Probar con Docker Localmente

### 2.1 Instalar Docker Desktop
- Windows/Mac: https://www.docker.com/products/docker-desktop
- Linux: https://docs.docker.com/engine/install/

### 2.2 Crear archivo .env local
```bash
cp .env.example .env
# Editar .env con tus valores reales
```

### 2.3 Construir y ejecutar
```bash
# Construir imagen
docker-compose build

# Iniciar servicios
docker-compose up

# Acceder a: http://localhost:8000
```

### 2.4 Comandos útiles
```bash
# Ver logs
docker-compose logs -f web

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Detener servicios
docker-compose down
```

---

## 🌐 PARTE 3: Despliegue en Render

### 3.1 Preparar repositorio GitHub

```bash
# Inicializar Git (si no lo has hecho)
git init

# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "Preparar proyecto para despliegue en Render con Neon PostgreSQL"

# Crear repositorio en GitHub
# Ve a https://github.com/new
# Nombra el repositorio: flash-marketplace

# Conectar y subir
git remote add origin https://github.com/TU_USUARIO/flash-marketplace.git
git branch -M main
git push -u origin main
```

### 3.2 Configurar Render

1. **Crear cuenta en Render**
   - Ve a https://render.com
   - Crea una cuenta (puedes usar GitHub)

2. **Crear nuevo Web Service**
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona "flash-marketplace"

3. **Configuración del servicio**
   ```
   Name: flash-marketplace
   Region: Oregon (US West) o la más cercana
   Branch: main
   Runtime: Docker
   Instance Type: Free (para empezar)
   ```

4. **Variables de entorno en Render**
   
   En "Environment" → "Add Environment Variable":
   
   ```
   DJANGO_SECRET_KEY=genera-una-clave-segura-con-50-caracteres-random
   DEBUG=False
   DJANGO_SETTINGS_MODULE=flash.settings.prod
   DATABASE_URL=postgresql://usuario:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
   ALLOWED_HOSTS=flash-marketplace.onrender.com,localhost
   PYTHON_VERSION=3.13.7
   ```

   Para generar SECRET_KEY:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Deploy**
   - Click en "Create Web Service"
   - Render automáticamente:
     - Detectará el Dockerfile
     - Construirá la imagen
     - Desplegará el contenedor
     - Asignará una URL: https://flash-marketplace.onrender.com

### 3.3 Configuración post-despliegue

#### Ejecutar migraciones
1. En Render Dashboard, ve a tu servicio
2. Ve a "Shell" en el menú lateral
3. Ejecuta:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

#### Cargar datos iniciales (si es necesario)
```bash
# En la Shell de Render
python manage.py loaddata data_backup.json
```

---

## 🔧 PARTE 4: Configuración de Archivos Estáticos y Media

### 4.1 WhiteNoise (ya configurado)
Los archivos estáticos se sirven automáticamente con WhiteNoise.

### 4.2 Archivos Media (subidas de usuarios)

Para producción, considera usar un servicio como:
- **AWS S3** (recomendado)
- **Cloudinary**
- **DigitalOcean Spaces**

#### Configurar S3 (opcional):
```python
# Instalar
pip install django-storages boto3

# En settings/prod.py
USE_S3 = os.environ.get('USE_S3', 'False') == 'True'

if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
```

---

## ✅ PARTE 5: Verificación Final

### 5.1 Checklist de despliegue
- [ ] Base de datos Neon creada y conectada
- [ ] Datos migrados desde SQLite
- [ ] Repositorio GitHub actualizado
- [ ] Render configurado con variables de entorno
- [ ] Servicio desplegado exitosamente
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Archivos estáticos funcionando
- [ ] URLs accesibles

### 5.2 Probar el sitio
1. Accede a tu URL: https://flash-marketplace.onrender.com
2. Verifica que cargue la página principal
3. Intenta iniciar sesión en el admin: /admin/
4. Verifica que las imágenes y CSS carguen correctamente
5. Prueba crear productos, hacer pedidos, etc.

### 5.3 Monitoreo
- **Logs en Render**: Dashboard → Logs (en tiempo real)
- **Métricas**: Dashboard → Metrics
- **Salud del servicio**: Render te notifica si el servicio se cae

---

## 🐛 PARTE 6: Solución de Problemas

### Error: "Application failed to respond"
```bash
# Verificar que Gunicorn esté instalado
pip freeze | grep gunicorn

# Verificar que el comando CMD en Dockerfile sea correcto
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "flash.wsgi:application"]
```

### Error: "No module named 'X'"
```bash
# Verificar requirements.txt
# Asegurar que todas las dependencias estén listadas
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Actualizar requirements.txt"
git push
```

### Error: "Database connection failed"
```bash
# Verificar DATABASE_URL en variables de entorno
# Debe incluir ?sslmode=require al final
# Formato: postgresql://user:pass@host/db?sslmode=require
```

### CSS/Imágenes no cargan
```bash
# En Render Shell
python manage.py collectstatic --noinput

# Verificar STATIC_ROOT y STATIC_URL en settings
# Asegurar que WhiteNoise esté en MIDDLEWARE
```

---

## 📚 Recursos Adicionales

- **Documentación de Render**: https://render.com/docs
- **Neon PostgreSQL**: https://neon.tech/docs
- **Django en producción**: https://docs.djangoproject.com/en/5.1/howto/deployment/
- **WhiteNoise**: http://whitenoise.evans.io/
- **Gunicorn**: https://docs.gunicorn.org/

---

## 🔄 Actualizaciones Futuras

Para actualizar tu aplicación después del despliegue inicial:

```bash
# 1. Hacer cambios en tu código local
# 2. Commit y push a GitHub
git add .
git commit -m "Descripción de cambios"
git push

# 3. Render detectará los cambios automáticamente
# 4. Rebuild y redeploy automático
```

---

## 💡 Consejos Finales

1. **Nunca commitees .env** - Úsalo solo localmente
2. **Usa .env.example** - Para documentar variables necesarias
3. **Monitorea los logs** - Especialmente después del primer despliegue
4. **Configura alertas** - Render puede enviarte notificaciones por email
5. **Haz backups** - Neon tiene backups automáticos, pero verifica
6. **Escala gradualmente** - Empieza con el tier gratuito
7. **HTTPS automático** - Render provee certificados SSL gratis

¡Buena suerte con tu despliegue! 🚀
