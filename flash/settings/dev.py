from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    # Apps del proyecto
    "apps.core",
    "apps.accounts",
    "apps.catalog",
    "apps.cart",
    "apps.orders",
    "apps.payments",
    "apps.reviews",
    "apps.search",
    # "products",  # Comentado por conflictos con apps.catalog
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",  # para pruebas en el navegador
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 12,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Configuración de drf-spectacular para documentación de API
SPECTACULAR_SETTINGS = {
    "TITLE": "Flash Marketplace API",
    "DESCRIPTION": "API para el marketplace Flash con gestión de productos, usuarios y pedidos",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/",
}

# Modelo de usuario personalizado - Comentado porque ya tenemos DB con User estándar
# AUTH_USER_MODEL = 'accounts.User'