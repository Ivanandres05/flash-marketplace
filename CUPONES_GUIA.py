"""
🎉 GUÍA DE PRUEBA: SISTEMA DE CUPONES FLASH MARKETPLACE
========================================================

El sistema de cupones está completamente funcional. Aquí están las instrucciones para probarlo:

📋 CUPONES CREADOS (listos para usar):
--------------------------------------

1. **FLASH10**
   - 10% de descuento en tu primera compra
   - Compra mínima: $50,000 COP
   - Descuento máximo: $50,000 COP
   - Válido por 30 días
   - Límite: 100 usos totales, 1 por usuario

2. **BIENVENIDO**
   - $20,000 COP de descuento fijo
   - Compra mínima: $100,000 COP
   - Válido por 60 días
   - Límite: 50 usos totales, 1 por usuario

3. **FLASH25**
   - 25% de descuento 
   - Compra mínima: $200,000 COP
   - Descuento máximo: $100,000 COP
   - Válido por 15 días
   - Límite: 30 usos totales, 2 por usuario

4. **NAVIDAD2025**
   - 30% de descuento especial
   - Compra mínima: $150,000 COP
   - Descuento máximo: $150,000 COP
   - Válido por 45 días
   - Sin límite de usos totales, 3 por usuario

5. **MEGA50**
   - $50,000 COP de descuento fijo
   - Compra mínima: $300,000 COP
   - Válido por 20 días
   - Límite: 20 usos totales, 1 por usuario


🧪 CÓMO PROBAR EL SISTEMA:
-------------------------

1. **INICIO DE SESIÓN**
   - Ve a: http://localhost:8080/cuenta/login/
   - Usuario: admin@example.com
   - Contraseña: (la que configuraste)

2. **AGREGAR PRODUCTOS AL CARRITO**
   - Ve a: http://localhost:8080/productos/
   - Agrega varios productos para alcanzar diferentes montos
   - Sugerencia: Agrega productos por $60,000 para probar FLASH10

3. **VER CUPONES DISPONIBLES**
   - Ve a: http://localhost:8080/pedidos/mis-cupones/
   - Verás todos los cupones con:
     * Código del cupón (click para copiar)
     * Porcentaje/monto de descuento
     * Fecha de validez
     * Compra mínima requerida
     * Estado de disponibilidad

4. **APLICAR CUPÓN EN EL CARRITO**
   - Ve a: http://localhost:8080/carrito/
   - En la sección "¿Tienes un cupón?":
     * Ingresa código: FLASH10
     * Click en "Aplicar"
   - Verás el descuento aplicado en tiempo real
   - El total se actualizará automáticamente

5. **VALIDACIONES AUTOMÁTICAS**
   El sistema valida:
   ✓ Cupón existe y está activo
   ✓ Fechas de validez (no expirado)
   ✓ Compra mínima alcanzada
   ✓ Usuario no excedió límite de usos
   ✓ Cupón no alcanzó límite global de usos


🔧 GESTIÓN DE CUPONES (ADMIN):
------------------------------

1. **ACCESO AL ADMIN**
   - Ve a: http://localhost:8080/admin/
   - Login: admin / tu_contraseña

2. **CREAR NUEVOS CUPONES**
   - Orders > Cupones > Agregar cupón
   - Configura:
     * Código único (ej: "VERANO2025")
     * Tipo de descuento (porcentaje/fijo)
     * Valor del descuento
     * Fechas de validez
     * Compra mínima
     * Límites de uso

3. **VER ESTADÍSTICAS**
   - En el listado de cupones verás:
     * Estado visual (activo/expirado)
     * Contador de usos
     * Indicadores de color según disponibilidad

4. **HISTORIAL DE USOS**
   - Orders > Usos de cupones
   - Ver quién usó cada cupón y cuándo


💡 ESCENARIOS DE PRUEBA SUGERIDOS:
----------------------------------

**Escenario 1: Primera compra con descuento**
- Carrito con $60,000 en productos
- Aplicar FLASH10
- Descuento: $6,000 (10%)
- Total final: $54,000

**Escenario 2: Compra grande con límite**
- Carrito con $1,000,000 en productos
- Aplicar FLASH10
- Descuento: $50,000 (límite máximo)
- Total final: $950,000

**Escenario 3: Descuento fijo**
- Carrito con $150,000 en productos
- Aplicar BIENVENIDO
- Descuento: $20,000 COP fijo
- Total final: $130,000

**Escenario 4: Cupón no válido**
- Carrito con $30,000 (menor a mínimo)
- Intentar aplicar FLASH10
- Resultado: Error "Compra mínima requerida: $50,000"

**Escenario 5: Cupón ya usado**
- Usar FLASH10 una vez
- Intentar usar FLASH10 nuevamente
- Resultado: Error "Ya has usado este cupón"


📊 FUNCIONALIDADES IMPLEMENTADAS:
---------------------------------

✅ Modelos de base de datos:
   - Coupon: Gestión completa de cupones
   - CouponUsage: Tracking de usos por usuario

✅ Validaciones de negocio:
   - Fechas de validez (from/to)
   - Compra mínima requerida
   - Límites de uso (global y por usuario)
   - Descuento máximo para porcentajes
   - Estado activo/inactivo

✅ Interfaz de usuario:
   - Página de cupones disponibles
   - Widget en el carrito para aplicar cupones
   - Indicadores visuales de estado
   - Copy-to-clipboard para códigos
   - Mensajes de error/éxito

✅ Admin Django:
   - CRUD completo de cupones
   - Indicadores visuales con colores
   - Filtros y búsqueda
   - Historial de usos (solo lectura)
   - Estadísticas de uso

✅ API/Endpoints:
   - POST /pedidos/cupones/validar/ - Aplicar cupón
   - POST /pedidos/cupones/eliminar/ - Quitar cupón
   - GET /pedidos/mis-cupones/ - Ver cupones disponibles

✅ Integración con carrito:
   - Cálculo automático de descuentos
   - Actualización en tiempo real
   - Persistencia en sesión
   - Validación antes de checkout


🚀 PRÓXIMOS PASOS SUGERIDOS:
----------------------------

1. Sistema de notificaciones por email cuando se recibe un cupón
2. Cupones personalizados por categoría de producto
3. Cupones de referido (invita amigos)
4. Cupones automáticos por cumpleaños
5. Dashboard de analytics de cupones
6. Cupones de "primera compra" automáticos


📝 NOTAS TÉCNICAS:
------------------

- Los cupones se almacenan en apps/orders/models.py
- Las vistas están en apps/orders/views.py
- El admin está en apps/orders/admin.py
- La plantilla está en templates/orders/my_coupons.html
- Integración con carrito en apps/cart/views.py y templates/cart/cart.html

- Base de datos: SQLite (tabla orders_coupon)
- Migraciones aplicadas: 0002_coupon_order_discount_amount_order_coupon_and_more
- Sin dependencias externas adicionales


¡DISFRUTA PROBANDO EL SISTEMA DE CUPONES! 🎉
"""

print(__doc__)
