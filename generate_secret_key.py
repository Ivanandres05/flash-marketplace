# Generar SECRET_KEY segura para Django
import secrets

secret_key = secrets.token_urlsafe(50)
print("Tu nueva SECRET_KEY:")
print(secret_key)
print("\nCópiala y pégala en tu archivo .env:")
print(f"SECRET_KEY={secret_key}")
