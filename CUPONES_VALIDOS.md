# 🎫 SISTEMA DE CUPONES - FLASH MARKETPLACE

## ✅ Cupones Actualizados y Válidos

Todos los cupones han sido actualizados y ahora están **100% funcionales** hasta el **30 de octubre de 2026**.

---

## 📋 CUPONES DISPONIBLES

### 1. **FLASH10** - Descuento del 10%
- **Código**: `FLASH10`
- **Descuento**: 10% de descuento
- **Compra mínima**: Sin mínimo
- **Límite de usos**: Ilimitado
- **Usos por usuario**: 1 vez
- **Estado**: ✅ **ACTIVO**

### 2. **BIENVENIDO** - Descuento de $5,000
- **Código**: `BIENVENIDO`
- **Descuento**: $5,000 COP fijo
- **Compra mínima**: Sin mínimo
- **Límite de usos**: Ilimitado
- **Usos por usuario**: 1 vez
- **Estado**: ✅ **ACTIVO**

### 3. **FLASH25** - Descuento del 25%
- **Código**: `FLASH25`
- **Descuento**: 25% de descuento
- **Compra mínima**: $50,000 COP
- **Descuento máximo**: $50,000 COP
- **Límite de usos**: Ilimitado
- **Usos por usuario**: 1 vez
- **Estado**: ✅ **ACTIVO**

### 4. **NAVIDAD2025** - Descuento del 30%
- **Código**: `NAVIDAD2025`
- **Descuento**: 30% de descuento
- **Compra mínima**: $100,000 COP
- **Descuento máximo**: $100,000 COP
- **Límite de usos**: Ilimitado
- **Usos por usuario**: 2 veces
- **Estado**: ✅ **ACTIVO**

### 5. **MEGA50** - Descuento del 50%
- **Código**: `MEGA50`
- **Descuento**: 50% de descuento
- **Compra mínima**: $200,000 COP
- **Descuento máximo**: $200,000 COP
- **Límite de usos**: 100 usos totales
- **Usos por usuario**: 1 vez
- **Estado**: ✅ **ACTIVO**

---

## 🚀 CÓMO USAR UN CUPÓN

### Paso 1: Agregar productos al carrito
1. Navega por el catálogo de productos
2. Agrega productos a tu carrito
3. Ve a **"Carrito"** (icono del carrito en el header)

### Paso 2: Aplicar el cupón
1. En la página del carrito, busca la sección **"¿Tienes un cupón?"**
2. Ingresa el código del cupón (ejemplo: `BIENVENIDO`)
3. Haz clic en **"Aplicar"**
4. El descuento se aplicará automáticamente

### Paso 3: Verificar el descuento
- El sistema mostrará:
  - ✅ Mensaje de éxito: "¡Cupón aplicado! Ahorras $X"
  - El subtotal original
  - El descuento aplicado
  - El total final con descuento

---

## 🔧 CAMBIOS IMPLEMENTADOS

### Modelo Cart (apps/cart/models.py)
```python
def get_total(self):
    """Calcula el total del carrito"""
    total = sum(item.product.price * item.quantity for item in self.items.all())
    return total

def get_item_count(self):
    """Retorna la cantidad total de items en el carrito"""
    return sum(item.quantity for item in self.items.all())
```

### Modelo CartItem (apps/cart/models.py)
```python
def get_subtotal(self):
    """Retorna el subtotal del item (precio * cantidad)"""
    return self.product.price * self.quantity
```

### Vista validate_coupon (apps/orders/views.py)
- ✅ Verifica que el usuario esté autenticado
- ✅ Valida que el carrito no esté vacío
- ✅ Verifica la compra mínima
- ✅ Calcula el descuento correctamente
- ✅ Guarda el cupón en la sesión
- ✅ Retorna mensajes claros de error

### Actualización de Cupones
- ✅ Todos los cupones tienen `is_active = True`
- ✅ `valid_from`: Ayer (29/10/2025)
- ✅ `valid_to`: En 1 año (30/10/2026)
- ✅ Lógica de validación funcionando

---

## ❌ ERRORES COMUNES Y SOLUCIONES

### Error: "Cupón no válido"
- **Causa**: El código ingresado no existe en la base de datos
- **Solución**: Verifica que hayas escrito el código correctamente (mayúsculas/minúsculas no importan)

### Error: "Debes iniciar sesión para usar cupones"
- **Causa**: No has iniciado sesión
- **Solución**: Haz clic en "Iniciar Sesión" en el header

### Error: "Tu carrito está vacío"
- **Causa**: No tienes productos en el carrito
- **Solución**: Agrega al menos un producto antes de aplicar un cupón

### Error: "Compra mínima requerida: $X"
- **Causa**: El total de tu carrito es menor al mínimo requerido
- **Solución**: Agrega más productos o usa otro cupón sin compra mínima (ejemplo: BIENVENIDO o FLASH10)

### Error: "Ya has usado este cupón el máximo de veces permitido"
- **Causa**: Ya has usado ese cupón antes
- **Solución**: Usa otro cupón disponible

### Error: "Este cupón ha alcanzado su límite de usos"
- **Causa**: El cupón MEGA50 tiene un límite de 100 usos totales
- **Solución**: Usa otro cupón disponible

---

## 🎯 PÁGINAS DONDE FUNCIONAN LOS CUPONES

1. **Carrito** (`/carrito/`): Página principal para aplicar cupones
2. **Checkout** (`/carrito/checkout/`): El cupón se mantiene en el proceso de pago
3. **Mis Cupones** (`/pedidos/mis-cupones/`): Ver cupones disponibles con información detallada

---

## 🧪 CÓMO PROBAR LOS CUPONES

### Test 1: Cupón sin compra mínima
```
1. Agrega cualquier producto al carrito (precio: $50,000)
2. Ve al carrito
3. Aplica cupón: BIENVENIDO
4. Resultado esperado: Descuento de $5,000 → Total: $45,000
```

### Test 2: Cupón con porcentaje
```
1. Agrega productos por $100,000 al carrito
2. Ve al carrito
3. Aplica cupón: FLASH10
4. Resultado esperado: Descuento de $10,000 (10%) → Total: $90,000
```

### Test 3: Cupón con compra mínima
```
1. Agrega productos por $150,000 al carrito
2. Ve al carrito
3. Aplica cupón: FLASH25
4. Resultado esperado: Descuento de $37,500 (25%) → Total: $112,500
```

### Test 4: Cupón con descuento máximo
```
1. Agrega productos por $500,000 al carrito
2. Ve al carrito
3. Aplica cupón: MEGA50
4. Resultado esperado: Descuento de $200,000 (máximo) → Total: $300,000
   (50% sería $250,000, pero el máximo es $200,000)
```

---

## 📊 ENDPOINTS API

### Validar Cupón
```
POST /pedidos/cupones/validar/
Parámetros:
  - code: Código del cupón (string)

Respuesta exitosa:
{
  "success": true,
  "message": "¡Cupón aplicado! Ahorras $5000",
  "discount": 5000.0,
  "new_total": 45000.0,
  "coupon_code": "BIENVENIDO"
}

Respuesta error:
{
  "success": false,
  "message": "Cupón no válido"
}
```

### Eliminar Cupón
```
POST /pedidos/cupones/eliminar/

Respuesta:
{
  "success": true,
  "message": "Cupón eliminado"
}
```

### Ver Mis Cupones
```
GET /pedidos/mis-cupones/

Retorna página HTML con lista de cupones disponibles
```

---

## 🔐 SEGURIDAD

- ✅ Validación de autenticación
- ✅ Validación de fechas (válido desde/hasta)
- ✅ Límites de uso por usuario
- ✅ Límites de uso global
- ✅ Validación de compra mínima
- ✅ Prevención de uso múltiple (se guarda en CouponUsage)
- ✅ Códigos case-insensitive (se convierten a mayúsculas)

---

## 📝 ADMINISTRACIÓN DE CUPONES

Para crear o editar cupones, accede al admin de Django:
```
URL: http://localhost:8080/admin/orders/coupon/
Usuario: admin
```

Campos importantes:
- **code**: Código único del cupón (automáticamente en mayúsculas)
- **discount_type**: 'percentage' o 'fixed'
- **discount_value**: Valor del descuento (% o monto fijo)
- **valid_from**: Fecha inicio de validez
- **valid_to**: Fecha fin de validez
- **min_purchase_amount**: Compra mínima requerida
- **max_discount_amount**: Descuento máximo (solo para porcentajes)
- **usage_limit**: Límite total de usos (null = ilimitado)
- **usage_limit_per_user**: Límite por usuario (default: 1)
- **is_active**: Activar/desactivar cupón

---

## ✨ ESTADO ACTUAL

🎉 **Sistema 100% funcional** 🎉

- ✅ 5 cupones activos y válidos
- ✅ Validación completa implementada
- ✅ Métodos get_total() y get_subtotal() agregados
- ✅ Manejo de errores mejorado
- ✅ Mensajes claros para el usuario
- ✅ Integración con carrito y checkout
- ✅ Página de "Mis Cupones" funcionando

---

**Última actualización**: 30 de octubre de 2025
**Estado del servidor**: ✅ Corriendo en http://localhost:8080/
