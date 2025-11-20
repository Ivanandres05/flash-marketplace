import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flash.settings.dev')
django.setup()

from django.contrib.auth.models import User
from apps.catalog.models import Category, Product
from apps.accounts.models import Profile

# Verificar si ya existen usuarios
if User.objects.count() == 0:
    # Crear superusuario
    print("Creando usuarios...")
    admin = User.objects.create_superuser('admin', 'admin@flashmarket.com', 'flash123')
    admin.first_name = 'Admin'
    admin.last_name = 'Flash'
    admin.save()

    # Crear usuarios regulares
    users_data = [
        ('juan', 'Juan', 'Pérez', 'juan@email.com'),
        ('maria', 'María', 'García', 'maria@email.com'),
        ('carlos', 'Carlos', 'López', 'carlos@email.com'),
    ]

    for username, first, last, email in users_data:
        user = User.objects.create_user(username, email, 'flash123')
        user.first_name = first
        user.last_name = last
        user.save()
        Profile.objects.create(user=user)

    print(f"✓ {User.objects.count()} usuarios creados")
else:
    print(f"✓ Ya existen {User.objects.count()} usuarios")

# Crear categorías
if Category.objects.count() == 0:
    print("\nCreando categorías...")
    categorias = ['Electrónicos', 'Ropa', 'Hogar', 'Deportes', 'Libros']

    for nombre in categorias:
        slug = nombre.lower().replace('ó', 'o').replace('í', 'i')
        Category.objects.create(name=nombre, slug=slug)

    print(f"✓ {Category.objects.count()} categorías creadas")
else:
    print(f"\n✓ Ya existen {Category.objects.count()} categorías")

# Crear productos con precios en COP
print("\nCreando productos con precios en COP...")

productos = [
    ('Audífonos Inalámbricos', 'Audífonos bluetooth con cancelación de ruido', 'Electrónicos', '149900'),
    ('Camiseta Deportiva', 'Camiseta de alta calidad para deporte', 'Ropa', '45900'),
    ('Laptop Gaming', 'Laptop de alto rendimiento', 'Electrónicos', '2999000'),
    ('Zapatillas Running', 'Zapatillas profesionales para running', 'Deportes', '299900'),
    ('Libro de Python', 'Aprende programación en Python', 'Libros', '89900'),
    ('Smartwatch', 'Reloj inteligente con múltiples funciones', 'Electrónicos', '499900'),
    ('Jeans Clásicos', 'Jeans de mezclilla de alta calidad', 'Ropa', '129900'),
    ('Cafetera Eléctrica', 'Cafetera automática programable', 'Hogar', '249900'),
    ('Bicicleta Montaña', 'Bicicleta profesional todo terreno', 'Deportes', '1899000'),
    ('Mochila Urbana', 'Mochila resistente para uso diario', 'Ropa', '79900'),
    ('Mouse Gamer', 'Mouse óptico de alta precisión', 'Electrónicos', '119900'),
    ('Vestido Elegante', 'Vestido para ocasiones especiales', 'Ropa', '199900'),
    ('Licuadora', 'Licuadora de alta potencia', 'Hogar', '189900'),
    ('Balón de Fútbol', 'Balón oficial de fútbol', 'Deportes', '69900'),
    ('Tablet 10"', 'Tablet con pantalla HD', 'Electrónicos', '799900'),
    ('Chaqueta de Cuero', 'Chaqueta de cuero genuino', 'Ropa', '399900'),
    ('Aspiradora Robot', 'Aspiradora inteligente automática', 'Hogar', '899900'),
    ('Set de Pesas', 'Juego completo de pesas ajustables', 'Deportes', '349900'),
    ('Cámara Digital', 'Cámara DSLR profesional', 'Electrónicos', '1999000'),
    ('Gafas de Sol', 'Gafas con protección UV', 'Ropa', '119900'),
    ('Lámpara LED', 'Lámpara inteligente con control remoto', 'Hogar', '149900'),
    ('Raqueta de Tenis', 'Raqueta profesional de tenis', 'Deportes', '279900'),
    ('Parlante Bluetooth', 'Parlante portátil con sonido 360°', 'Electrónicos', '199900'),
    ('Bufanda de Lana', 'Bufanda tejida a mano', 'Ropa', '54900'),
    ('Juego de Sábanas', 'Sábanas de algodón egipcio', 'Hogar', '179900'),
]

for nombre, desc, cat_name, precio in productos:
    categoria = Category.objects.get(name=cat_name)
    slug = nombre.lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('"', '')
    Product.objects.create(
        name=nombre,
        description=desc,
        price=Decimal(precio),
        category=categoria,
        stock=100,
        slug=slug
    )

print(f"✓ {Product.objects.count()} productos creados")
print(f"\n✅ Base de datos configurada correctamente con precios en COP")
print(f"\nUsuarios creados (todos con contraseña 'flash123'):")
for user in User.objects.all():
    print(f"  - {user.username}")
