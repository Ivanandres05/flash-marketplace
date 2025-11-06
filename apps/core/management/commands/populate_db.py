# Comando management para poblar la base de datos con datos de prueba
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.catalog.models import Category, Product, ProductImage
from apps.reviews.models import Review
from apps.accounts.models import Profile, Address
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba para Flash Marketplace'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando población de base de datos...'))

        # Crear usuarios
        self.stdout.write('Creando usuarios...')
        users = []
        
        # Admin
        admin = User.objects.filter(username='admin').first()
        if not admin:
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@flash.com',
                password='admin123',
                first_name='Admin',
                last_name='Flash'
            )
            self.stdout.write(self.style.SUCCESS(f'Usuario admin creado'))
        users.append(admin)

        # Usuarios normales
        user_names = [
            ('juan', 'Juan', 'Pérez', 'juan@example.com'),
            ('maria', 'María', 'García', 'maria@example.com'),
            ('carlos', 'Carlos', 'López', 'carlos@example.com'),
            ('ana', 'Ana', 'Martínez', 'ana@example.com'),
            ('pedro', 'Pedro', 'Rodríguez', 'pedro@example.com'),
        ]

        for username, first_name, last_name, email in user_names:
            user = User.objects.filter(username=username).first()
            if not user:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Crear perfil
                Profile.objects.create(
                    user=user,
                    address=f'Calle {random.randint(1, 100)}',
                    phone_number=f'300{random.randint(1000000, 9999999)}'
                )
                
                # Crear dirección
                Address.objects.create(
                    user=user,
                    street=f'Carrera {random.randint(1, 50)} #{random.randint(1, 100)}-{random.randint(1, 99)}',
                    city='Bogotá',
                    state='Cundinamarca',
                    zip_code=f'1100{random.randint(10, 99)}'
                )
                
                self.stdout.write(self.style.SUCCESS(f'Usuario {username} creado'))
            users.append(user)

        # Crear categorías
        self.stdout.write('Creando categorías...')
        categories_data = [
            ('Electrónica', 'electronica'),
            ('Moda', 'moda'),
            ('Hogar y Cocina', 'hogar-cocina'),
            ('Deportes', 'deportes'),
            ('Libros', 'libros'),
            ('Juguetes', 'juguetes'),
            ('Belleza', 'belleza'),
            ('Oficina', 'oficina'),
        ]

        categories = []
        for name, slug in categories_data:
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoría {name} creada'))

        # Crear productos
        self.stdout.write('Creando productos...')
        products_data = [
            # Electrónica
            ('Smartphone Galaxy X', categories[0], 899.99, 'Smartphone de última generación con cámara de 108MP', 50),
            ('Laptop Pro 15"', categories[0], 1299.99, 'Laptop potente para profesionales', 30),
            ('Auriculares Bluetooth', categories[0], 79.99, 'Auriculares inalámbricos con cancelación de ruido', 100),
            ('Tablet 10 pulgadas', categories[0], 349.99, 'Tablet ideal para entretenimiento', 75),
            ('Smartwatch Fit', categories[0], 199.99, 'Reloj inteligente con monitor de salud', 120),
            
            # Moda
            ('Zapatillas Running Pro', categories[1], 89.99, 'Zapatillas deportivas de alto rendimiento', 200),
            ('Jeans Clásicos', categories[1], 49.99, 'Jeans de mezclilla cómodos', 150),
            ('Chaqueta de Cuero', categories[1], 159.99, 'Chaqueta elegante de cuero genuino', 50),
            ('Camisa Formal', categories[1], 39.99, 'Camisa perfecta para oficina', 180),
            ('Vestido de Verano', categories[1], 69.99, 'Vestido fresco y elegante', 90),
            
            # Hogar
            ('Cafetera Automática', categories[2], 129.99, 'Cafetera programable con molinillo', 80),
            ('Juego de Sartenes', categories[2], 89.99, 'Set de 5 sartenes antiadherentes', 100),
            ('Aspiradora Robot', categories[2], 299.99, 'Limpieza automática inteligente', 60),
            ('Licuadora Potente', categories[2], 79.99, 'Licuadora de 1200W', 110),
            ('Lámpara LED Inteligente', categories[2], 45.99, 'Iluminación controlable por app', 150),
            
            # Deportes
            ('Bicicleta de Montaña', categories[3], 599.99, 'Bicicleta 21 velocidades', 40),
            ('Mancuernas Ajustables', categories[3], 129.99, 'Set de mancuernas de 5-25kg', 70),
            ('Yoga Mat Premium', categories[3], 29.99, 'Esterilla antideslizante', 200),
            ('Balón de Fútbol', categories[3], 24.99, 'Balón profesional tamaño 5', 250),
            ('Raqueta de Tenis', categories[3], 89.99, 'Raqueta para principiantes', 90),
            
            # Libros
            ('El Programador Pragmático', categories[4], 34.99, 'Libro esencial para desarrolladores', 150),
            ('Cien Años de Soledad', categories[4], 19.99, 'Clásico de García Márquez', 200),
            ('Sapiens', categories[4], 29.99, 'Historia de la humanidad', 180),
            ('Hábitos Atómicos', categories[4], 24.99, 'Libro de desarrollo personal', 220),
            ('El Principito', categories[4], 14.99, 'Clásico infantil', 300),
        ]

        products = []
        for name, category, price, description, stock in products_data:
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'slug': name.lower().replace(' ', '-'),
                    'description': description,
                    'price': Decimal(str(price)),
                    'stock': stock,
                    'available': True
                }
            )
            products.append(product)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Producto {name} creado'))

        # Crear reviews
        self.stdout.write('Creando reseñas...')
        comments = [
            'Excelente producto, superó mis expectativas.',
            'Muy buena calidad, lo recomiendo totalmente.',
            'Buen producto pero el envío tardó un poco.',
            'Perfecto, justo lo que necesitaba.',
            'Calidad precio muy buena.',
            'Me encanta, volveré a comprar.',
            'Cumple con lo prometido.',
            'Buena compra, satisfecho con el producto.',
            'Recomendado al 100%',
            'Excelente servicio y producto de calidad.',
        ]

        review_count = 0
        for product in products[:15]:  # Reviews para los primeros 15 productos
            num_reviews = random.randint(2, 8)
            for _ in range(num_reviews):
                user = random.choice(users)
                rating = random.randint(3, 5)
                comment = random.choice(comments)
                
                Review.objects.get_or_create(
                    product=product,
                    user=user,
                    defaults={
                        'rating': rating,
                        'comment': comment
                    }
                )
                review_count += 1

        self.stdout.write(self.style.SUCCESS(f'{review_count} reseñas creadas'))

        # Resumen
        self.stdout.write(self.style.SUCCESS('\n=== RESUMEN ==='))
        self.stdout.write(self.style.SUCCESS(f'Usuarios: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Categorías: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Productos: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Reseñas: {Review.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('\n✅ Base de datos poblada exitosamente!'))
        self.stdout.write(self.style.WARNING('\nCredenciales de prueba:'))
        self.stdout.write(self.style.WARNING('Admin: admin / admin123'))
        self.stdout.write(self.style.WARNING('Usuarios: juan, maria, carlos, ana, pedro / password123'))
