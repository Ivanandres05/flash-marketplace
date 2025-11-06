"""
Script para verificar que el proyecto está listo para despliegue
"""
import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Verifica si un archivo existe"""
    exists = Path(file_path).exists()
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {file_path}")
    return exists

def check_env_var(var_name):
    """Verifica si una variable de entorno está configurada"""
    value = os.getenv(var_name)
    exists = value is not None and value != ""
    status = "✓" if exists else "✗"
    print(f"{status} Variable {var_name}: {'Configurada' if exists else 'NO configurada'}")
    return exists

def main():
    print("=" * 60)
    print("Verificación de Preparación para Despliegue")
    print("=" * 60)
    print()
    
    checks_passed = 0
    total_checks = 0
    
    # Verificar archivos de configuración
    print("📁 Archivos de Configuración:")
    print("-" * 60)
    files_to_check = [
        ("Dockerfile", "Dockerfile"),
        ("docker-compose.yml", "Docker Compose"),
        (".env.example", "Template de variables de entorno"),
        ("requirements.txt", "Dependencias"),
        ("flash/settings/prod.py", "Configuración de producción"),
        (".gitignore", "Git ignore"),
        ("DEPLOYMENT_GUIDE.md", "Guía de despliegue"),
    ]
    
    for file_path, description in files_to_check:
        if check_file_exists(file_path, description):
            checks_passed += 1
        total_checks += 1
    
    print()
    
    # Verificar archivo .env
    print("🔐 Variables de Entorno:")
    print("-" * 60)
    
    if Path(".env").exists():
        print("✓ Archivo .env existe")
        checks_passed += 1
        
        # Cargar variables del archivo .env
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            env_vars = [
                "SECRET_KEY",
                "DEBUG",
                "DATABASE_URL",
                "ALLOWED_HOSTS",
            ]
            
            for var in env_vars:
                if check_env_var(var):
                    checks_passed += 1
                total_checks += 1
                
        except ImportError:
            print("⚠ python-dotenv no instalado, no se pueden verificar variables")
    else:
        print("✗ Archivo .env NO existe")
        print("  Crea uno desde .env.example: cp .env.example .env")
    
    total_checks += 1
    print()
    
    # Verificar que .env no esté en git
    print("🔒 Seguridad:")
    print("-" * 60)
    
    try:
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
            if ".env" in gitignore_content:
                print("✓ .env está en .gitignore")
                checks_passed += 1
            else:
                print("✗ .env NO está en .gitignore - ¡PELIGRO!")
    except FileNotFoundError:
        print("✗ .gitignore no encontrado")
    
    total_checks += 1
    print()
    
    # Verificar dependencias de producción
    print("📦 Dependencias de Producción:")
    print("-" * 60)
    
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            
            prod_deps = [
                ("gunicorn", "Servidor WSGI"),
                ("whitenoise", "Archivos estáticos"),
                ("dj-database-url", "Configuración de DB"),
                ("psycopg", "Driver PostgreSQL"),
            ]
            
            for dep, description in prod_deps:
                if dep in requirements:
                    print(f"✓ {description} ({dep})")
                    checks_passed += 1
                else:
                    print(f"✗ {description} ({dep}) - NO encontrado")
                total_checks += 1
    except FileNotFoundError:
        print("✗ requirements.txt no encontrado")
    
    print()
    
    # Verificar apps instaladas
    print("🐍 Apps de Django:")
    print("-" * 60)
    
    apps = [
        "apps.accounts",
        "apps.catalog",
        "apps.cart",
        "apps.orders",
        "apps.payments",
        "apps.reviews",
        "apps.search",
        "apps.core",
    ]
    
    for app in apps:
        app_path = Path(app.replace(".", "/"))
        if app_path.exists():
            print(f"✓ {app}")
            checks_passed += 1
        else:
            print(f"✗ {app} - NO encontrada")
        total_checks += 1
    
    print()
    print("=" * 60)
    print(f"Resultado: {checks_passed}/{total_checks} verificaciones pasadas")
    print("=" * 60)
    
    if checks_passed == total_checks:
        print("\n✅ ¡Todo listo para despliegue!")
        print("\nSiguientes pasos:")
        print("1. python migrate_to_neon.py  (migrar a PostgreSQL)")
        print("2. git push origin main  (subir a GitHub)")
        print("3. Configurar en Render siguiendo DEPLOYMENT_GUIDE.md")
        return 0
    else:
        print(f"\n⚠ Faltan {total_checks - checks_passed} elementos")
        print("\nRevisa los items marcados con ✗ y corrige antes de desplegar")
        return 1

if __name__ == "__main__":
    sys.exit(main())
