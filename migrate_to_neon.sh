#!/bin/bash

# Script para migrar datos de SQLite a Neon PostgreSQL

echo "======================================"
echo "Migración de SQLite a Neon PostgreSQL"
echo "======================================"
echo ""

# 1. Exportar datos desde SQLite
echo "1. Exportando datos desde SQLite..."
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --exclude auth.permission \
    --exclude contenttypes \
    --exclude admin.logentry \
    --exclude sessions.session \
    --indent 2 \
    > backup_data.json

if [ $? -eq 0 ]; then
    echo "✓ Datos exportados correctamente a backup_data.json"
else
    echo "✗ Error al exportar datos"
    exit 1
fi

echo ""
echo "2. Configura tu DATABASE_URL en el archivo .env con la conexión a Neon"
echo "   Ejemplo: DATABASE_URL=postgresql://user:pass@host.neon.tech/dbname?sslmode=require"
echo ""
read -p "¿Has configurado DATABASE_URL en .env? (s/n): " confirm

if [ "$confirm" != "s" ]; then
    echo "Configura DATABASE_URL primero y vuelve a ejecutar el script"
    exit 1
fi

# 3. Crear tablas en Neon
echo ""
echo "3. Creando tablas en Neon PostgreSQL..."
python manage.py migrate --settings=flash.settings.prod

if [ $? -eq 0 ]; then
    echo "✓ Tablas creadas correctamente"
else
    echo "✗ Error al crear tablas"
    exit 1
fi

# 4. Importar datos a Neon
echo ""
echo "4. Importando datos a Neon PostgreSQL..."
python manage.py loaddata backup_data.json --settings=flash.settings.prod

if [ $? -eq 0 ]; then
    echo "✓ Datos importados correctamente"
else
    echo "✗ Error al importar datos"
    exit 1
fi

echo ""
echo "======================================"
echo "✓ Migración completada exitosamente"
echo "======================================"
echo ""
echo "Siguiente paso: Verifica que todo funcione correctamente"
echo "  python manage.py createsuperuser --settings=flash.settings.prod"
echo "  python manage.py runserver --settings=flash.settings.prod"
