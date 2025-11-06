#!/bin/bash

# Esperar a que la base de datos esté lista
echo "Esperando a PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL iniciado"

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario si no existe
echo "Verificando superusuario..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@flash.com', 'flash123')
    print('Superusuario creado')
else:
    print('Superusuario ya existe')
END

# Iniciar servidor
echo "Iniciando servidor..."
exec gunicorn flash.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile - --error-logfile -
