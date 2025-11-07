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
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p staticfiles media logs

# Exponer puerto
EXPOSE 8000

# Script de inicio
CMD python manage.py migrate --noinput --settings=flash.settings.prod && \
    python manage.py fix_ivan_email --settings=flash.settings.prod && \
    python manage.py collectstatic --noinput --settings=flash.settings.prod && \
    gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 120 --log-level info flash.wsgi:application
