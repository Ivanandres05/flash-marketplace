# Usar imagen oficial de Python
FROM python:3.13.7-slim

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p staticfiles media logs

# Recolectar archivos estáticos (fallar silenciosamente si hay error)
RUN python manage.py collectstatic --noinput --settings=flash.settings.prod || echo "Collectstatic failed, will run later"

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar migraciones y servidor
CMD python manage.py migrate --noinput --settings=flash.settings.prod && \
    python manage.py collectstatic --noinput --settings=flash.settings.prod && \
    gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 flash.wsgi:application
