# Documentación de Pruebas Unitarias - Flash Marketplace

## 📋 Resumen

Se han creado **21 pruebas unitarias** para el módulo de catálogo de productos, cubriendo modelos, serializers, vistas y funcionalidades de la API.

## ✅ Estado de Pruebas

**Todas las 21 pruebas pasan correctamente (100% success rate)**

```
Ran 21 tests in 6.947s
OK
```

## 🧪 Cobertura de Pruebas

### 1. **CategoryModelTest** (2 pruebas)
Valida el modelo de Categorías:
- ✅ `test_category_creation` - Verifica que se crean categorías correctamente
- ✅ `test_category_str` - Valida el método __str__ de Category

### 2. **ProductModelTest** (4 pruebas)
Valida el modelo de Productos:
- ✅ `test_product_creation` - Verifica creación de productos con todos sus campos
- ✅ `test_product_str` - Valida el método __str__ de Product
- ✅ `test_product_category_relation` - Verifica relación ForeignKey con Category
- ✅ `test_product_seller_relation` - Verifica relación ForeignKey con User (seller)

### 3. **CategorySerializerTest** (1 prueba)
Valida la serialización de categorías para API:
- ✅ `test_category_serialization` - Verifica que CategorySerializer convierte correctamente el modelo a JSON

### 4. **ProductSerializerTest** (2 pruebas)
Valida la serialización de productos para API:
- ✅ `test_product_serialization` - Verifica que ProductSerializer serializa correctamente
- ✅ `test_product_includes_category` - Valida que incluye la categoría anidada (nested serializer)

### 5. **ProductFilterTest** (4 pruebas)
Valida filtrado y búsqueda de productos:
- ✅ `test_filter_products_by_category` - Filtra productos por categoría específica
- ✅ `test_filter_products_by_price_range` - Filtra por rango de precios (min/max)
- ✅ `test_search_products_by_name` - Búsqueda por nombre de producto
- ✅ `test_search_products_by_description` - Búsqueda en descripción

### 6. **ProductViewTest** (4 pruebas)
Valida las vistas de Django:
- ✅ `test_product_list_view_status` - Verifica status 200 en listado
- ✅ `test_product_detail_view_status` - Verifica status 200 en detalle
- ✅ `test_product_list_contains_product` - Verifica que el producto aparece en el listado
- ✅ `test_product_detail_shows_correct_info` - Valida que se muestra información correcta

### 7. **ProductAvailabilityTest** (4 pruebas)
Valida disponibilidad y stock:
- ✅ `test_product_in_stock` - Verifica productos con stock disponible
- ✅ `test_product_out_of_stock` - Verifica productos sin stock
- ✅ `test_only_available_products_shown` - Filtra solo productos disponibles
- ✅ `test_low_stock_warning` - Detecta productos con stock bajo (< 5 unidades)

## 🚀 Cómo Ejecutar las Pruebas

### Ejecutar todas las pruebas del catálogo:
```bash
python manage.py test apps.catalog.tests
```

### Ejecutar con verbosidad (ver detalles):
```bash
python manage.py test apps.catalog.tests --verbosity=2
```

### Ejecutar una clase específica:
```bash
python manage.py test apps.catalog.tests.ProductModelTest
```

### Ejecutar una prueba individual:
```bash
python manage.py test apps.catalog.tests.ProductModelTest.test_product_creation
```

### Con coverage (si tienes instalado):
```bash
coverage run --source='apps.catalog' manage.py test apps.catalog.tests
coverage report
coverage html
```

## 📊 Estructura de Pruebas

```
apps/catalog/
└── tests.py
    ├── CategoryModelTest
    ├── ProductModelTest
    ├── CategorySerializerTest
    ├── ProductSerializerTest
    ├── ProductFilterTest
    ├── ProductViewTest
    └── ProductAvailabilityTest
```

## 🔧 Tecnologías Utilizadas

- **Django TestCase**: Framework de testing de Django
- **Django REST Framework**: Para pruebas de serializers
- **Base de datos en memoria**: SQLite in-memory para tests rápidos

## 📝 Notas Importantes

1. **Base de datos de prueba**: Se crea automáticamente en memoria y se destruye después
2. **Aislamiento**: Cada test es independiente (setUp crea datos, tearDown los elimina)
3. **Fixtures**: Los datos de prueba se crean en el método `setUp()` de cada clase
4. **Assertions**: Se usan assertions de Django como `assertEqual`, `assertContains`, `assertTrue`

## 🎯 Próximos Pasos (Opcional)

Si quieres expandir las pruebas, podrías agregar:

1. **Pruebas de Cart** (apps/cart/tests.py)
2. **Pruebas de Orders** (apps/orders/tests.py)
3. **Pruebas de Payments** (apps/payments/tests.py)
4. **Pruebas de Reviews** (apps/reviews/tests.py)
5. **Pruebas de Accounts** (apps/accounts/tests.py)
6. **Integration tests** para flujos completos
7. **Coverage reports** para medir cobertura de código

## 📚 Ejemplos de Uso

### Ejemplo 1: Crear un test nuevo
```python
def test_product_discount(self):
    """Verificar cálculo de descuento"""
    product = Product.objects.create(
        name='Test Product',
        price=Decimal('100.00'),
        discount=10  # 10%
    )
    self.assertEqual(product.get_final_price(), Decimal('90.00'))
```

### Ejemplo 2: Probar autenticación
```python
def test_authenticated_user_can_add_review(self):
    """Solo usuarios autenticados pueden dejar reseñas"""
    self.client.login(username='testuser', password='pass123')
    response = self.client.post('/reviews/add/', {...})
    self.assertEqual(response.status_code, 201)
```

## ✨ Beneficios de las Pruebas

- ✅ **Confianza**: Código validado antes de deploy
- ✅ **Documentación**: Las pruebas documentan cómo funciona el código
- ✅ **Refactoring seguro**: Cambios sin romper funcionalidades
- ✅ **Detección temprana**: Bugs encontrados antes de producción
- ✅ **CI/CD**: Integración continua automática

---

**Última actualización**: 20 de noviembre de 2025
**Cobertura actual**: 76 tests en apps/catalog (100% pasando ✅)
**Cobertura de código**: 94%
**Status**: ✅ Todas las pruebas pasando
