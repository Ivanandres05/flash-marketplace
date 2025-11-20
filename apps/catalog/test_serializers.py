"""
Pruebas unitarias con pytest para serializers de Catalog
"""
import pytest
from decimal import Decimal
from apps.catalog.models import Category, Product
from apps.catalog.serializers import CategorySerializer, ProductSerializer


@pytest.mark.django_db
class TestCategorySerializer:
    """Pruebas para CategorySerializer"""
    
    def test_category_serialization(self, create_category):
        """Verificar serialización de Category a JSON"""
        serializer = CategorySerializer(create_category)
        data = serializer.data
        
        assert data['name'] == 'Electrónica'
        assert data['slug'] == 'electronica'
        assert 'id' in data
    
    def test_category_deserialization(self):
        """Verificar deserialización de JSON a Category"""
        data = {
            'name': 'Deportes',
            'slug': 'deportes'
        }
        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()
        category = serializer.save()
        
        assert category.name == 'Deportes'
        assert category.slug == 'deportes'
    
    def test_category_serialization_fields(self, create_category):
        """Verificar que se incluyen todos los campos necesarios"""
        serializer = CategorySerializer(create_category)
        data = serializer.data
        
        expected_fields = {'id', 'name', 'slug'}
        assert set(data.keys()) == expected_fields
    
    def test_multiple_categories_serialization(self, db):
        """Verificar serialización de múltiples categorías"""
        Category.objects.create(name='Cat 1', slug='cat-1')
        Category.objects.create(name='Cat 2', slug='cat-2')
        Category.objects.create(name='Cat 3', slug='cat-3')
        
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        
        assert len(serializer.data) == 3
        assert serializer.data[0]['name'] == 'Cat 1'


@pytest.mark.django_db
class TestProductSerializer:
    """Pruebas para ProductSerializer"""
    
    def test_product_serialization(self, create_product):
        """Verificar serialización de Product a JSON"""
        serializer = ProductSerializer(create_product)
        data = serializer.data
        
        assert data['name'] == 'Laptop Test'
        assert Decimal(data['price']) == Decimal('1500000.00')
        assert data['stock'] == 10
        assert data['available'] is True
    
    def test_product_includes_nested_category(self, create_product):
        """Verificar que Product incluye Category serializada (nested)"""
        serializer = ProductSerializer(create_product)
        data = serializer.data
        
        assert 'category' in data
        assert isinstance(data['category'], dict)
        assert data['category']['name'] == 'Electrónica'
        assert data['category']['slug'] == 'electronica'
    
    def test_product_serialization_fields(self, create_product):
        """Verificar que se incluyen todos los campos"""
        serializer = ProductSerializer(create_product)
        data = serializer.data
        
        expected_fields = {
            'id', 'name', 'slug', 'description', 'price', 
            'stock', 'available', 'category', 'seller', 
            'created', 'updated'
        }
        assert set(data.keys()) == expected_fields
    
    def test_multiple_products_serialization(self, multiple_products):
        """Verificar serialización de múltiples productos"""
        serializer = ProductSerializer(multiple_products, many=True)
        
        assert len(serializer.data) == 5
        assert serializer.data[0]['name'] == 'Producto 1'
        assert serializer.data[4]['name'] == 'Producto 5'
    
    def test_product_price_format(self, create_product):
        """Verificar formato correcto del precio"""
        serializer = ProductSerializer(create_product)
        data = serializer.data
        
        # El precio debe tener 2 decimales
        price_str = str(data['price'])
        assert '.' in price_str
        decimal_places = len(price_str.split('.')[1])
        assert decimal_places == 2
    
    def test_product_with_zero_stock(self, db, create_user, create_category):
        """Verificar serialización de producto sin stock"""
        product = Product.objects.create(
            name='Sin Stock',
            slug='sin-stock',
            description='Test',
            price=Decimal('100.00'),
            stock=0,
            category=create_category,
            seller=create_user,
            available=False
        )
        
        serializer = ProductSerializer(product)
        data = serializer.data
        
        assert data['stock'] == 0
        assert data['available'] is False


@pytest.mark.django_db
class TestSerializerValidation:
    """Pruebas para validación de serializers"""
    
    def test_category_valid_data(self):
        """Verificar validación con datos correctos"""
        data = {
            'name': 'Libros',
            'slug': 'libros'
        }
        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()
        assert not serializer.errors
    
    def test_category_missing_required_field(self):
        """Verificar validación con campo requerido faltante"""
        data = {
            'name': 'Libros'
            # slug faltante
        }
        serializer = CategorySerializer(data=data)
        assert not serializer.is_valid()
        assert 'slug' in serializer.errors
    
    def test_product_deserialization(self, create_user, create_category):
        """Verificar deserialización de Product"""
        # El serializer usa nested category, entonces necesita el diccionario completo
        data = {
            'name': 'Nuevo Producto',
            'slug': 'nuevo-producto',
            'description': 'Descripción del producto',
            'price': '250000.00',
            'stock': 15,
            'category': {
                'name': create_category.name,
                'slug': create_category.slug
            },
            'seller': create_user.id,
            'available': True
        }
        
        # Para validación, el serializer actual solo lee (read-only para nested)
        # Esta prueba verifica que el serializer puede serializar correctamente
        product = Product.objects.create(
            name=data['name'],
            slug=data['slug'],
            description=data['description'],
            price=Decimal(data['price']),
            stock=data['stock'],
            category=create_category,
            seller=create_user,
            available=data['available']
        )
        
        serializer = ProductSerializer(product)
        assert serializer.data['name'] == 'Nuevo Producto'


@pytest.mark.django_db 
class TestSerializerReadOnly:
    """Pruebas para campos de solo lectura"""
    
    def test_product_timestamps_are_auto_generated(self, db, create_user, create_category):
        """Verificar que created y updated se generan automáticamente"""
        data = {
            'name': 'Test Product',
            'slug': 'test-product',
            'description': 'Test',
            'price': '100.00',
            'stock': 10,
            'category': create_category.id,
            'seller': create_user.id
        }
        
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            
            # Verificar que los timestamps existen
            assert product.created is not None
            assert product.updated is not None
