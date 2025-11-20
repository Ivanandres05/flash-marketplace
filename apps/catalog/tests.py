"""
Pruebas unitarias completas para la API de Productos - Flash Marketplace
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal

from apps.catalog.models import Product, Category
from apps.catalog.serializers import ProductSerializer, CategorySerializer


class CategoryModelTest(TestCase):
    """Pruebas para el modelo Category"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Electrónica",
            slug="electronica"
        )
    
    def test_category_creation(self):
        """Verificar que una categoría se crea correctamente"""
        self.assertEqual(self.category.name, "Electrónica")
        self.assertEqual(self.category.slug, "electronica")
        self.assertTrue(isinstance(self.category, Category))
    
    def test_category_str(self):
        """Verificar el método __str__ de Category"""
        self.assertEqual(str(self.category), "Electrónica")


class ProductModelTest(TestCase):
    """Pruebas para el modelo Product"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Tecnología",
            slug="tecnologia"
        )
        self.product = Product.objects.create(
            name="Laptop Dell",
            slug="laptop-dell",
            description="Laptop de alta gama",
            price=Decimal('2500000.00'),
            stock=10,
            category=self.category,
            seller=self.user,
            available=True
        )
    
    def test_product_creation(self):
        """Verificar que un producto se crea correctamente"""
        self.assertEqual(self.product.name, "Laptop Dell")
        self.assertEqual(self.product.price, Decimal('2500000.00'))
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.available)
    
    def test_product_str(self):
        """Verificar el método __str__ de Product"""
        self.assertEqual(str(self.product), "Laptop Dell")
    
    def test_product_category_relation(self):
        """Verificar relación con Category"""
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.category.name, "Tecnología")
    
    def test_product_seller_relation(self):
        """Verificar relación con User (seller)"""
        self.assertEqual(self.product.seller, self.user)


class CategorySerializerTest(TestCase):
    """Pruebas para CategorySerializer"""
    
    def setUp(self):
        self.category_data = {
            'name': 'Deportes',
            'slug': 'deportes'
        }
        self.category = Category.objects.create(**self.category_data)
    
    def test_category_serialization(self):
        """Verificar serialización de Category"""
        serializer = CategorySerializer(self.category)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Deportes')
        self.assertEqual(data['slug'], 'deportes')
        self.assertIn('id', data)


class ProductSerializerTest(TestCase):
    """Pruebas para ProductSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='pass123'
        )
        self.category = Category.objects.create(
            name='Hogar',
            slug='hogar'
        )
        self.product = Product.objects.create(
            name='Mesa de Madera',
            slug='mesa-madera',
            description='Mesa robusta',
            price=Decimal('350000.00'),
            stock=5,
            category=self.category,
            seller=self.user,
            available=True
        )
    
    def test_product_serialization(self):
        """Verificar serialización de Product"""
        serializer = ProductSerializer(self.product)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Mesa de Madera')
        self.assertEqual(Decimal(data['price']), Decimal('350000.00'))
        self.assertEqual(data['stock'], 5)
        self.assertTrue(data['available'])
    
    def test_product_includes_category(self):
        """Verificar que Product incluye Category serializada"""
        serializer = ProductSerializer(self.product)
        data = serializer.data
        
        self.assertIn('category', data)
        self.assertEqual(data['category']['name'], 'Hogar')


class ProductFilterTest(TestCase):
    """Pruebas para filtrado y búsqueda de productos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@example.com',
            password='apipass123'
        )
        self.category1 = Category.objects.create(
            name='Juguetes',
            slug='juguetes'
        )
        self.category2 = Category.objects.create(
            name='Libros',
            slug='libros'
        )
        self.product1 = Product.objects.create(
            name='Muñeca',
            slug='muneca',
            description='Muñeca de colección',
            price=Decimal('80000.00'),
            stock=20,
            category=self.category1,
            seller=self.user,
            available=True
        )
        self.product2 = Product.objects.create(
            name='Carro de Juguete',
            slug='carro-juguete',
            description='Carro a control remoto',
            price=Decimal('150000.00'),
            stock=15,
            category=self.category1,
            seller=self.user,
            available=True
        )
        self.product3 = Product.objects.create(
            name='Python para Todos',
            slug='python-para-todos',
            description='Libro de programación',
            price=Decimal('45000.00'),
            stock=100,
            category=self.category2,
            seller=self.user,
            available=True
        )
    
    def test_filter_products_by_category(self):
        """Verificar filtrado por categoría"""
        products_toys = Product.objects.filter(category=self.category1)
        products_books = Product.objects.filter(category=self.category2)
        
        self.assertEqual(products_toys.count(), 2)
        self.assertEqual(products_books.count(), 1)
    
    def test_filter_products_by_price_range(self):
        """Verificar filtrado por rango de precio"""
        products = Product.objects.filter(
            price__gte=Decimal('100000.00'),
            price__lte=Decimal('200000.00')
        )
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, 'Carro de Juguete')
    
    def test_search_products_by_name(self):
        """Verificar búsqueda por nombre"""
        from django.db.models import Q
        query = "python"
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, 'Python para Todos')
    
    def test_search_products_by_description(self):
        """Verificar búsqueda por descripción"""
        from django.db.models import Q
        query = "control remoto"
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, 'Carro de Juguete')


class ProductViewTest(TestCase):
    """Pruebas para las vistas de productos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='viewuser',
            email='view@example.com',
            password='viewpass123'
        )
        self.category = Category.objects.create(
            name='Ropa',
            slug='ropa'
        )
        self.product = Product.objects.create(
            name='Camisa Azul',
            slug='camisa-azul',
            description='Camisa de algodón',
            price=Decimal('45000.00'),
            stock=50,
            category=self.category,
            seller=self.user,
            available=True
        )
    
    def test_product_list_view_status(self):
        """Verificar que la vista de listado responde correctamente"""
        url = reverse('catalog:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_product_detail_view_status(self):
        """Verificar que la vista de detalle responde correctamente"""
        url = reverse('catalog:product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_product_list_contains_product(self):
        """Verificar que el listado contiene el producto"""
        url = reverse('catalog:product-list')
        response = self.client.get(url)
        self.assertContains(response, 'Camisa Azul')
    
    def test_product_detail_shows_correct_info(self):
        """Verificar que el detalle muestra información correcta"""
        url = reverse('catalog:product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertContains(response, 'Camisa Azul')


class ProductAvailabilityTest(TestCase):
    """Pruebas para disponibilidad y stock de productos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='stockuser',
            email='stock@example.com',
            password='stockpass123'
        )
        self.category = Category.objects.create(
            name='Electrodomésticos',
            slug='electrodomesticos'
        )
    
    def test_product_in_stock(self):
        """Verificar producto con stock disponible"""
        product = Product.objects.create(
            name='Licuadora',
            slug='licuadora',
            price=Decimal('150000.00'),
            stock=10,
            category=self.category,
            seller=self.user,
            available=True
        )
        self.assertTrue(product.available)
        self.assertGreater(product.stock, 0)
    
    def test_product_out_of_stock(self):
        """Verificar producto sin stock"""
        product = Product.objects.create(
            name='Tostadora',
            slug='tostadora',
            price=Decimal('75000.00'),
            stock=0,
            category=self.category,
            seller=self.user,
            available=False
        )
        self.assertFalse(product.available)
        self.assertEqual(product.stock, 0)
    
    def test_only_available_products_shown(self):
        """Verificar que solo se muestran productos disponibles en queryset"""
        Product.objects.create(
            name='Microondas Disponible',
            slug='microondas-disponible',
            price=Decimal('300000.00'),
            stock=5,
            category=self.category,
            seller=self.user,
            available=True
        )
        Product.objects.create(
            name='Microondas No Disponible',
            slug='microondas-no-disponible',
            price=Decimal('300000.00'),
            stock=0,
            category=self.category,
            seller=self.user,
            available=False
        )
        
        available_products = Product.objects.filter(available=True)
        self.assertEqual(available_products.count(), 1)
        self.assertEqual(available_products.first().name, 'Microondas Disponible')
    
    def test_low_stock_warning(self):
        """Verificar detección de stock bajo"""
        product = Product.objects.create(
            name='Cafetera',
            slug='cafetera',
            price=Decimal('120000.00'),
            stock=3,
            category=self.category,
            seller=self.user,
            available=True
        )
        # Stock bajo si es menor a 5 unidades
        self.assertLess(product.stock, 5)
        self.assertTrue(product.available)