"""
Script para migrar datos de SQLite a Neon PostgreSQL
Ejecutar desde el directorio raíz del proyecto
"""
import os
import sys
import django
import subprocess

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completado")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error en {description}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("=" * 50)
    print("Migración de SQLite a Neon PostgreSQL")
    print("=" * 50)
    
    # 1. Exportar datos desde SQLite
    if not run_command(
        'python manage.py dumpdata '
        '--natural-foreign '
        '--natural-primary '
        '--exclude auth.permission '
        '--exclude contenttypes '
        '--exclude admin.logentry '
        '--exclude sessions.session '
        '--indent 2 '
        '> backup_data.json',
        "1. Exportando datos desde SQLite"
    ):
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("PASO IMPORTANTE:")
    print("=" * 50)
    print("Configura DATABASE_URL en tu archivo .env con la conexión a Neon")
    print("Ejemplo:")
    print("  DATABASE_URL=postgresql://user:pass@host.neon.tech/dbname?sslmode=require")
    print("=" * 50)
    
    input("\nPresiona Enter cuando hayas configurado DATABASE_URL...")
    
    # Cambiar a configuración de producción
    os.environ['DJANGO_SETTINGS_MODULE'] = 'flash.settings.prod'
    
    # 2. Crear tablas en Neon
    if not run_command(
        'python manage.py migrate --settings=flash.settings.prod',
        "2. Creando tablas en Neon PostgreSQL"
    ):
        sys.exit(1)
    
    # 3. Importar datos a Neon
    if not run_command(
        'python manage.py loaddata backup_data.json --settings=flash.settings.prod',
        "3. Importando datos a Neon PostgreSQL"
    ):
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✓ Migración completada exitosamente")
    print("=" * 50)
    print("\nSiguientes pasos:")
    print("1. Verifica los datos: python manage.py shell --settings=flash.settings.prod")
    print("2. Crea superusuario si es necesario: python manage.py createsuperuser --settings=flash.settings.prod")
    print("3. Prueba el servidor: python manage.py runserver --settings=flash.settings.prod")

if __name__ == '__main__':
    main()
