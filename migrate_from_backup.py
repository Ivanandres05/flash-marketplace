#!/usr/bin/env python
"""
Script para importar datos a Neon PostgreSQL
EJECUTAR DESPUÉS DE migrate_to_neon.py y configurar DATABASE_URL
"""
import os
import sys
import django

# Setup Django con settings de producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.prod')
django.setup()

from django.core.management import call_command

def import_from_backup():
    print("=" * 50)
    print("IMPORTANDO DATOS A NEON POSTGRESQL")
    print("=" * 50)
    
    # Verificar que existe el archivo de backup
    if not os.path.exists('data_backup.json'):
        print("❌ ERROR: No se encontró data_backup.json")
        print("   Primero ejecuta: python migrate_to_neon.py")
        sys.exit(1)
    
    # Paso 1: Ejecutar migraciones
    print("\n1. Ejecutando migraciones en Neon...")
    call_command('migrate')
    print("✓ Migraciones completadas")
    
    # Paso 2: Cargar datos
    print("\n2. Cargando datos...")
    call_command('loaddata', 'data_backup.json')
    print("✓ Datos importados exitosamente")
    
    print("\n3. LISTO! Tu base de datos en Neon está configurada")
    print("\n" + "=" * 50)

if __name__ == '__main__':
    import_from_backup()
