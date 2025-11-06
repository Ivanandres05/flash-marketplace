# ⚡ Flash Marketplace# ⚡ Flash Marketplace# Mi Proyecto



> Plataforma e-commerce moderna estilo Amazon construida con Django 5.1



## 🚀 Características> Plataforma e-commerce moderna estilo Amazon construida con Django 5.1Este proyecto es una aplicación desarrollada en TypeScript. A continuación se presentan las instrucciones para ejecutar y utilizar la aplicación.



- ✅ Sistema de autenticación completo (registro, login, perfil)

- ✅ Catálogo de productos con búsqueda y filtros

- ✅ Carrito de compras funcional con AJAX## 🚀 Características## Estructura del Proyecto

- ✅ Sistema de checkout y gestión de órdenes

- ✅ Panel de administración de Django

- ✅ Sistema de reseñas de productos

- ✅ Diseño responsive (Bootstrap 5.3)- ✅ Sistema de autenticación completo (registro, login, perfil)- `src/app.ts`: Punto de entrada de la aplicación.

- ✅ API REST con documentación Swagger/ReDoc

- ✅ Gestión de stock en tiempo real- ✅ Catálogo de productos con búsqueda y filtros- `src/types/index.ts`: Tipos e interfaces utilizados en el proyecto.



## 📋 Requisitos Previos- ✅ Carrito de compras funcional (con AJAX)- `tsconfig.json`: Configuración de TypeScript.



- Python 3.11 o superior- ✅ Sistema de checkout y órdenes- `package.json`: Configuración de npm.

- pip (gestor de paquetes de Python)

- Git- ✅ Panel de administración de Django



## 🔧 Instalación Rápida- ✅ Sistema de reseñas de productos## Instalación



### 1. Clonar y configurar- ✅ Diseño responsive (Bootstrap 5.3)



```bash- ✅ Context processors para carrito globalPara instalar las dependencias del proyecto, ejecuta el siguiente comando en la raíz del proyecto:

# Clonar repositorio

git clone <repository-url>- ✅ Gestión de stock en tiempo real

cd Flash

```

# Crear entorno virtual

python -m venv .venv## 📋 Requisitos Previosnpm install



# Activar entorno virtual```

# Windows:

.venv\Scripts\activate- Python 3.11 o superior

# Linux/Mac:

source .venv/bin/activate- pip (gestor de paquetes de Python)## Ejecución



# Instalar dependencias

pip install -r requirements.txt

```## 🔧 Instalación RápidaPara ejecutar la aplicación, utiliza el siguiente comando:



### 2. Configurar base de datos



```bash### 1. Clonar y configurar```

# Aplicar migraciones

python manage.py migratenpm start



# Crear superusuario (opcional)```bash```

python manage.py createsuperuser

# Clonar repositorio

# Poblar con datos de prueba (recomendado)

python manage.py populate_dbgit clone <repository-url>Asegúrate de que el entorno esté configurado correctamente y que todas las dependencias estén instaladas antes de ejecutar la aplicación.

```

cd Flash

### 3. Ejecutar servidor

## Contribuciones

```bash

python manage.py runserver 8080# Crear entorno virtual

```

python -m venv .venvLas contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

**¡Listo!** Visita: http://127.0.0.1:8080/



## 👥 Credenciales de Prueba

# Activar entorno virtual## Licencia

**Admin:** `admin` / `admin123`  

**Usuarios:** `juan`, `maria`, `carlos`, `ana`, `pedro` / `password123`# Windows:



## 📁 Estructura del Proyecto.venv\Scripts\activateEste proyecto está bajo la licencia MIT.

# Linux/Mac:

```source .venv/bin/activate

Flash/

├── apps/                    # Aplicaciones Django# Instalar dependencias

│   ├── accounts/           # Autenticación y perfilespip install -r requirements.txt

│   ├── cart/               # Carrito de compras```

│   ├── catalog/            # Productos y categorías

│   ├── core/               # Funcionalidad base### 2. Configurar base de datos

│   ├── orders/             # Gestión de pedidos

│   ├── payments/           # Procesamiento de pagos```bash

│   ├── reviews/            # Sistema de reseñas# Aplicar migraciones

│   └── search/             # Búsqueda de productospython manage.py migrate

├── flash/                  # Configuración del proyecto

│   ├── settings/           # Configuraciones (base, dev, prod)# Crear superusuario (opcional)

│   ├── urls.py             # URLs principalespython manage.py createsuperuser

│   ├── wsgi.py             # WSGI para producción

│   └── asgi.py             # ASGI para async# Poblar con datos de prueba (recomendado)

├── static/                 # Archivos estáticospython manage.py populate_db

│   ├── css/                # Estilos CSS```

│   └── js/                 # JavaScript

├── templates/              # Plantillas HTML### 3. Ejecutar servidor

│   ├── accounts/           # Templates de usuarios

│   ├── cart/               # Templates del carrito```bash

│   ├── catalog/            # Templates de productospython manage.py runserver 8080

│   └── base.html           # Template base```

├── .venv/                  # Entorno virtual (no en git)

├── db.sqlite3              # Base de datos SQLite**¡Listo!** Visita: http://127.0.0.1:8080/

├── manage.py               # CLI de Django

└── requirements.txt        # Dependencias Python## 👥 Credenciales de Prueba

```

**Admin:** `admin` / `admin123`  

## 🎨 Stack Tecnológico**Usuarios:** `juan`, `maria`, `carlos` / `password123`



- **Backend:** Django 5.1.2, Django REST Framework 3.16.1## 📁 Estructura del Proyecto

- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción recomendado)

- **Frontend:** Bootstrap 5.3, Font Awesome 6.4, JavaScript (Vanilla)```

- **Docs API:** drf-spectacular (Swagger/ReDoc)Flash/

- **Otros:** django-filter, django-cors-headers, Pillow├── apps/               # Aplicaciones Django

│   ├── accounts/      # Autenticación

## 📝 Comandos Útiles│   ├── cart/          # Carrito

│   ├── catalog/       # Productos

```bash│   ├── orders/        # Pedidos

# Crear migraciones│   └── ...

python manage.py makemigrations├── flash/             # Configuración

│   └── settings/      # base, dev, prod

# Aplicar migraciones├── static/            # CSS, JS, imágenes

python manage.py migrate├── templates/         # HTML

└── manage.py

# Limpiar y recargar DB```

rm db.sqlite3

python manage.py migrate## 🎨 Stack Tecnológico

python manage.py populate_db

- **Backend:** Django 5.1, DRF, SQLite

# Colectar archivos estáticos (para producción)- **Frontend:** Bootstrap 5.3, Font Awesome, Vanilla JS

python manage.py collectstatic --no-input- **Docs API:** drf-spectacular (Swagger/ReDoc)



# Ejecutar tests## 📝 Comandos Útiles

python manage.py test

```bash

# Shell interactivo de Django# Crear migraciones

python manage.py shellpython manage.py makemigrations

```

# Limpiar y recargar DB

## 🔍 URLs Principalesrm db.sqlite3

python manage.py migrate

### Frontendpython manage.py populate_db

- **Home:** http://127.0.0.1:8080/

- **Productos:** http://127.0.0.1:8080/productos/# Colectar archivos estáticos

- **Carrito:** http://127.0.0.1:8080/carrito/python manage.py collectstatic

- **Login:** http://127.0.0.1:8080/cuenta/login/

- **Registro:** http://127.0.0.1:8080/cuenta/register/# Ejecutar tests

- **Perfil:** http://127.0.0.1:8080/cuenta/perfil/python manage.py test

- **Admin:** http://127.0.0.1:8080/admin/```



### API Documentation## 🔍 APIs Disponibles

- **Swagger UI:** http://127.0.0.1:8080/api/docs/

- **ReDoc:** http://127.0.0.1:8080/api/redoc/- Swagger: http://127.0.0.1:8080/api/docs/

- **Schema JSON:** http://127.0.0.1:8080/api/schema/- ReDoc: http://127.0.0.1:8080/api/redoc/

- Schema: http://127.0.0.1:8080/api/schema/

## 🚢 Despliegue a Producción

## 🚢 Producción

### 1. Configurar variables de entorno

1. Configurar variables en `.env`:

Crear archivo `.env` en la raíz:```env

SECRET_KEY=tu-clave-secreta

```envDEBUG=False

SECRET_KEY=tu-clave-secreta-muy-seguraALLOWED_HOSTS=tudominio.com

DEBUG=FalseDATABASE_URL=postgresql://...

ALLOWED_HOSTS=tudominio.com,www.tudominio.com```

DATABASE_URL=postgresql://user:password@localhost/dbname

```2. Usar configuración de producción:

```bash

### 2. Usar configuración de producciónexport DJANGO_SETTINGS_MODULE=flash.settings.prod

python manage.py collectstatic --no-input

```bash```

export DJANGO_SETTINGS_MODULE=flash.settings.prod

python manage.py collectstatic --no-input## 📱 Funcionalidades

python manage.py migrate

```✅ Carrito AJAX en tiempo real  

✅ Notificaciones visuales  

### 3. Servidor WSGI (Gunicorn recomendado)✅ Filtros y búsqueda  

✅ Gestión de stock  

```bash✅ Checkout completo  

pip install gunicorn✅ Sistema de reseñas  

gunicorn flash.wsgi:application --bind 0.0.0.0:8000

```## 📄 Licencia



## 📱 Funcionalidades ImplementadasMIT License - Flash Marketplace 2025



✅ Carrito de compras con AJAX  ## ⭐ Dale una estrella

✅ Notificaciones visuales en tiempo real  

✅ Filtros por categoría y precio  Si te fue útil, ¡dale una ⭐ en GitHub!

✅ Búsqueda de productos  
✅ Gestión automática de stock  
✅ Checkout con múltiples métodos de pago  
✅ Sistema de reseñas con calificaciones  
✅ Perfil de usuario con historial de pedidos  
✅ Panel de administración completo  

## 🛠️ Próximas Mejoras Sugeridas

- [ ] Integración con pasarelas de pago reales (Stripe, PayPal)
- [ ] Sistema de notificaciones por email
- [ ] Panel de vendedor para múltiples vendedores
- [ ] Sistema de cupones y descuentos
- [ ] Wishlist / Lista de deseos
- [ ] Comparador de productos
- [ ] Búsqueda avanzada con Elasticsearch
- [ ] Tests unitarios y de integración
- [ ] CI/CD con GitHub Actions
- [ ] Dockerización (opcional)

## 📄 Licencia

MIT License - Flash Marketplace 2025

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## ⭐ Soporte

Si este proyecto te fue útil, ¡dale una ⭐ en GitHub!

---

**Desarrollado con ❤️ usando Django**
