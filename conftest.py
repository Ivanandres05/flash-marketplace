"""
Configuración de fixtures globales para pytest-django
"""
import pytest
from django.contrib.auth.models import User
from decimal import Decimal
from apps.catalog.models import Category, Product


@pytest.fixture
def user_data():
    """Datos básicos de usuario para tests"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }


@pytest.fixture
def create_user(db, user_data):
    """Fixture para crear un usuario de prueba"""
    return User.objects.create_user(**user_data)


@pytest.fixture
def authenticated_client(client, create_user, user_data):
    """Cliente autenticado para tests"""
    client.login(username=user_data['username'], password=user_data['password'])
    return client


@pytest.fixture
def category_data():
    """Datos básicos de categoría"""
    return {
        'name': 'Electrónica',
        'slug': 'electronica'
    }


@pytest.fixture
def create_category(db, category_data):
    """Fixture para crear una categoría"""
    return Category.objects.create(**category_data)


@pytest.fixture
def product_data(create_user, create_category):
    """Datos básicos de producto"""
    return {
        'name': 'Laptop Test',
        'slug': 'laptop-test',
        'description': 'Laptop de prueba',
        'price': Decimal('1500000.00'),
        'stock': 10,
        'category': create_category,
        'seller': create_user,
        'available': True
    }


@pytest.fixture
def create_product(db, product_data):
    """Fixture para crear un producto"""
    return Product.objects.create(**product_data)


@pytest.fixture
def multiple_products(db, create_user, create_category):
    """Fixture para crear múltiples productos"""
    products = []
    for i in range(5):
        product = Product.objects.create(
            name=f'Producto {i+1}',
            slug=f'producto-{i+1}',
            description=f'Descripción del producto {i+1}',
            price=Decimal(f'{(i+1)*100000}.00'),
            stock=10 + i,
            category=create_category,
            seller=create_user,
            available=True
        )
        products.append(product)
    return products
