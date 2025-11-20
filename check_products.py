import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from apps.catalog.models import Product

products = Product.objects.all()[:15]
for p in products:
    print(f'{p.id}: {p.name} - Categoría: {p.category.name}')
