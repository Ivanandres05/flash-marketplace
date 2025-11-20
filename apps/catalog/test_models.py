"""
Pruebas unitarias con pytest para modelos de Catalog
"""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from apps.catalog.models import Category, Product


@pytest.mark.django_db
class TestCategoryModel:
    """Pruebas para el modelo Category"""
    
    def test_category_creation(self, create_category):
        """Verificar que una categoría se crea correctamente"""
        assert create_category.name == "Electrónica"
        assert create_category.slug == "electronica"
        assert isinstance(create_category, Category)
    
    def test_category_str(self, create_category):
        """Verificar el método __str__ de Category"""
        assert str(create_category) == "Electrónica"
    
    def test_category_has_products_relation(self, create_category, create_product):
        """Verificar que Category tiene relación con productos"""
        assert create_category.products.count() == 1
        assert create_product in create_category.products.all()


@pytest.mark.django_db
class TestProductModel:
    """Pruebas para el modelo Product"""
    
    def test_product_creation(self, create_product):
        """Verificar que un producto se crea correctamente"""
        assert create_product.name == "Laptop Test"
        assert create_product.price == Decimal('1500000.00')
        assert create_product.stock == 10
        assert create_product.available is True
    
    def test_product_str(self, create_product):
        """Verificar el método __str__ de Product"""
        assert str(create_product) == "Laptop Test"
    
    def test_product_category_relation(self, create_product, create_category):
        """Verificar relación con Category"""
        assert create_product.category == create_category
        assert create_product.category.name == "Electrónica"
    
    def test_product_seller_relation(self, create_product, create_user):
        """Verificar relación con User (seller)"""
        assert create_product.seller == create_user
        assert create_product.seller.username == 'testuser'
    
    def test_product_get_seller_name(self, create_product):
        """Verificar método get_seller_name()"""
        seller_name = create_product.get_seller_name()
        assert seller_name == "Flash Marketplace"
    
    def test_product_default_values(self, db, create_user, create_category):
        """Verificar valores por defecto del producto"""
        product = Product.objects.create(
            name='Producto Default',
            slug='producto-default',
            description='Test',
            price=Decimal('100.00'),
            stock=5,
            category=create_category,
            seller=create_user
        )
        assert product.available is True
        assert product.created is not None
        assert product.updated is not None


@pytest.mark.django_db
class TestProductQueries:
    """Pruebas para queries de productos"""
    
    def test_filter_by_category(self, multiple_products, create_category):
        """Verificar filtrado por categoría"""
        products = Product.objects.filter(category=create_category)
        assert products.count() == 5
    
    def test_filter_by_price_range(self, multiple_products):
        """Verificar filtrado por rango de precios"""
        products = Product.objects.filter(
            price__gte=Decimal('200000.00'),
            price__lte=Decimal('400000.00')
        )
        assert products.count() == 3
    
    def test_filter_available_products(self, db, create_user, create_category):
        """Verificar filtrado de productos disponibles"""
        Product.objects.create(
            name='Disponible 1',
            slug='disponible-1',
            description='Test',
            price=Decimal('100.00'),
            stock=10,
            category=create_category,
            seller=create_user,
            available=True
        )
        Product.objects.create(
            name='No Disponible',
            slug='no-disponible',
            description='Test',
            price=Decimal('100.00'),
            stock=0,
            category=create_category,
            seller=create_user,
            available=False
        )
        
        available = Product.objects.filter(available=True)
        assert available.count() == 1
    
    def test_order_by_price(self, multiple_products):
        """Verificar ordenamiento por precio"""
        products = Product.objects.all().order_by('price')
        prices = [p.price for p in products]
        assert prices == sorted(prices)
    
    def test_search_by_name(self, db, create_user, create_category):
        """Verificar búsqueda por nombre"""
        Product.objects.create(
            name='Laptop Gaming',
            slug='laptop-gaming',
            description='Test',
            price=Decimal('100.00'),
            stock=5,
            category=create_category,
            seller=create_user
        )
        Product.objects.create(
            name='Mouse Inalámbrico',
            slug='mouse-inalambrico',
            description='Test',
            price=Decimal('50.00'),
            stock=10,
            category=create_category,
            seller=create_user
        )
        
        laptops = Product.objects.filter(name__icontains='laptop')
        assert laptops.count() == 1
        assert laptops.first().name == 'Laptop Gaming'


@pytest.mark.django_db
class TestProductStock:
    """Pruebas para manejo de stock"""
    
    def test_product_in_stock(self, create_product):
        """Verificar producto con stock"""
        assert create_product.stock > 0
        assert create_product.available is True
    
    def test_product_out_of_stock(self, db, create_user, create_category):
        """Verificar producto sin stock"""
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
        assert product.stock == 0
        assert product.available is False
    
    def test_low_stock_detection(self, db, create_user, create_category):
        """Verificar detección de stock bajo"""
        product = Product.objects.create(
            name='Stock Bajo',
            slug='stock-bajo',
            description='Test',
            price=Decimal('100.00'),
            stock=3,
            category=create_category,
            seller=create_user
        )
        assert product.stock < 5
        assert product.available is True
    
    @pytest.mark.parametrize("stock,expected_available", [
        (0, False),
        (1, True),
        (5, True),
        (100, True),
    ])
    def test_stock_availability_scenarios(self, db, create_user, create_category, stock, expected_available):
        """Probar diferentes escenarios de stock"""
        product = Product.objects.create(
            name=f'Test Stock {stock}',
            slug=f'test-stock-{stock}',
            description='Test',
            price=Decimal('100.00'),
            stock=stock,
            category=create_category,
            seller=create_user,
            available=expected_available
        )
        assert product.stock == stock
        assert product.available == expected_available
