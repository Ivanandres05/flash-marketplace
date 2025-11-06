# ✅ Checklist de Despliegue - Flash Marketplace

Usa este checklist para asegurarte de que todo está listo para producción.

## 📋 Pre-Despliegue

### Configuración Local
- [ ] Python 3.13+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Todas las dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Variables de entorno configuradas en `.env`
- [ ] SECRET_KEY generada (ejecutar `python generate_secret_key.py`)
- [ ] Proyecto funciona localmente (`python manage.py runserver`)

### Base de Datos
- [ ] Cuenta en Neon creada (https://neon.tech)
- [ ] Base de datos PostgreSQL creada en Neon
- [ ] DATABASE_URL copiada desde Neon
- [ ] DATABASE_URL incluye `?sslmode=require`
- [ ] Datos exportados desde SQLite (`python manage.py dumpdata`)
- [ ] Migraciones aplicadas en Neon (`python manage.py migrate --settings=flash.settings.prod`)
- [ ] Datos importados a Neon (`python manage.py loaddata backup_data.json`)
- [ ] Verificada la conexión a Neon

### Docker
- [ ] Docker instalado
- [ ] Dockerfile creado y revisado
- [ ] docker-compose.yml configurado
- [ ] Imagen construida exitosamente (`docker build -t flash-marketplace .`)
- [ ] Probado localmente con docker-compose (`docker-compose up`)
- [ ] Contenedor funciona correctamente

### Git y GitHub
- [ ] Cuenta en GitHub
- [ ] Repositorio creado en GitHub
- [ ] `.gitignore` actualizado
- [ ] `.env` NO está en el repositorio (verificar con `git status`)
- [ ] Código subido a GitHub (`git push origin main`)

## 🚀 Despliegue en Render

### Configuración Inicial
- [ ] Cuenta en Render creada (https://render.com)
- [ ] Repositorio de GitHub conectado a Render
- [ ] Web Service creado
- [ ] Environment configurado como "Docker"
- [ ] Instance Type seleccionado

### Variables de Entorno en Render
Verifica que todas estas variables estén configuradas:

- [ ] `DEBUG=False`
- [ ] `SECRET_KEY=tu-secret-key-generada`
- [ ] `DJANGO_SETTINGS_MODULE=flash.settings.prod`
- [ ] `DATABASE_URL=postgresql://...?sslmode=require`
- [ ] `ALLOWED_HOSTS=.onrender.com`
- [ ] `SITE_URL=https://tu-app.onrender.com`
- [ ] `STATIC_ROOT=/app/staticfiles`
- [ ] `MEDIA_ROOT=/app/media`

### Primer Despliegue
- [ ] Deploy iniciado en Render
- [ ] Build completado sin errores
- [ ] Servicio en estado "Live"
- [ ] URL de la app accesible

### Post-Despliegue
- [ ] Acceder al Shell de Render
- [ ] Ejecutar `python manage.py migrate`
- [ ] Ejecutar `python manage.py collectstatic --noinput`
- [ ] Crear superusuario (`python manage.py createsuperuser`)
- [ ] Verificar que la app carga
- [ ] Verificar que los archivos estáticos cargan
- [ ] Probar login
- [ ] Probar panel administrativo

## 🔍 Verificación Final

### Funcionalidad
- [ ] Página principal carga correctamente
- [ ] Login funciona
- [ ] Registro funciona
- [ ] Catálogo de productos se muestra
- [ ] Búsqueda funciona
- [ ] Carrito funciona
- [ ] Sistema de cupones funciona
- [ ] Checkout funciona
- [ ] Panel de vendedor accesible
- [ ] Panel administrativo accesible (solo admin)
- [ ] Reseñas se muestran

### Archivos Estáticos
- [ ] CSS carga correctamente
- [ ] JavaScript funciona
- [ ] Iconos (Font Awesome) se muestran
- [ ] Imágenes cargan

### Seguridad
- [ ] HTTPS habilitado (automático en Render)
- [ ] DEBUG=False en producción
- [ ] SECRET_KEY es única y segura
- [ ] .env NO está en GitHub
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] Cookies seguras habilitadas
- [ ] HSTS headers configurados

### Base de Datos
- [ ] Conexión a Neon PostgreSQL funciona
- [ ] Usuarios pueden registrarse
- [ ] Datos persisten correctamente
- [ ] No hay errores de conexión en logs

## 📊 Monitoreo

### Logs de Render
- [ ] Revisar logs en busca de errores
- [ ] Verificar que no hay warnings críticos
- [ ] Confirmar que Gunicorn está corriendo

### Performance
- [ ] Página carga en tiempo razonable (<3 segundos)
- [ ] Sin errores 500
- [ ] Sin errores 404 inesperados

## 🐛 Troubleshooting

### Si algo falla:

**Build Error en Render:**
```bash
# Verifica Dockerfile
# Revisa requirements.txt
# Chequea logs de build
```

**Error 500:**
```bash
# Revisa logs de Render
# Verifica variables de entorno
# Confirma DATABASE_URL
```

**Static Files no cargan:**
```bash
# En Shell de Render:
python manage.py collectstatic --noinput
```

**Bad Request (400):**
```bash
# Verifica ALLOWED_HOSTS
# Debe incluir .onrender.com
```

## 📝 Notas

### URLs Importantes:
- **App:** https://tu-app.onrender.com
- **Admin:** https://tu-app.onrender.com/admin/
- **Panel Admin:** https://tu-app.onrender.com/admin-dashboard/

### Credenciales:
- **Superusuario:** (crear en Shell de Render)
- **Database:** Neon Console
- **Render:** Dashboard

### Documentación:
- [ ] README.md actualizado
- [ ] DEPLOYMENT_GUIDE.md revisado
- [ ] Comentarios en código claros

## ✅ Checklist Completado

Fecha: _____________

Desplegado por: _____________

URL de producción: _____________

---

¡Felicidades! 🎉 Tu aplicación Flash Marketplace está en producción.
