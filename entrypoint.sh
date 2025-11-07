#!/bin/bash

# Script de inicio para Render - Ejecuta migraciones automáticamente

echo "🚀 Iniciando Flash Marketplace..."

# Ejecutar migraciones
echo "📊 Aplicando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar servidor con Gunicorn
echo "✅ Iniciando servidor..."
gunicorn flash.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
