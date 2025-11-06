from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('canceled', 'Cancelado'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Tarjeta de Crédito/Débito'),
        ('pse', 'PSE'),
        ('cash', 'Efectivo'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Información de envío
    shipping_address = models.TextField(default='')
    shipping_city = models.CharField(max_length=100, default='')
    shipping_state = models.CharField(max_length=100, default='')
    shipping_zip_code = models.CharField(max_length=10, default='')
    shipping_phone = models.CharField(max_length=15, default='')
    
    # Información de pago
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')
    
    # Totales
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Notas adicionales
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Pedido #{self.id} - {self.user.username}'
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity}x {self.product.name} en Pedido #{self.order.id}'
    
    @property
    def subtotal(self):
        return self.quantity * self.price
    
    def get_total(self):
        """Retorna el total del item (cantidad * precio)"""
        return self.quantity * self.price


class Coupon(models.Model):
    """Sistema de cupones de descuento para el marketplace"""
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Porcentaje'),
        ('fixed', 'Monto Fijo'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    description = models.TextField(blank=True, verbose_name='Descripción')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor de Descuento',
        help_text='Porcentaje (1-100) o Monto Fijo en COP'
    )
    
    # Validez temporal
    valid_from = models.DateTimeField(verbose_name='Válido Desde')
    valid_to = models.DateTimeField(verbose_name='Válido Hasta')
    
    # Restricciones de uso
    min_purchase_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Monto Mínimo de Compra',
        help_text='Compra mínima requerida en COP'
    )
    max_discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name='Descuento Máximo',
        help_text='Descuento máximo aplicable (solo para porcentajes)'
    )
    usage_limit = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name='Límite de Usos Total',
        help_text='Número máximo de veces que se puede usar este cupón'
    )
    usage_limit_per_user = models.PositiveIntegerField(
        default=1,
        verbose_name='Límite por Usuario',
        help_text='Número máximo de veces que cada usuario puede usar este cupón'
    )
    times_used = models.PositiveIntegerField(default=0, verbose_name='Veces Usado')
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'
    
    def __str__(self):
        if self.discount_type == 'percentage':
            return f'{self.code} - {self.discount_value}% OFF'
        return f'{self.code} - ${self.discount_value:,.0f} COP OFF'
    
    def is_valid(self):
        """Verifica si el cupón es válido en este momento"""
        now = timezone.now()
        if not self.is_active:
            return False, 'Este cupón no está activo'
        if now < self.valid_from:
            return False, f'Este cupón será válido desde {self.valid_from.strftime("%d/%m/%Y")}'
        if now > self.valid_to:
            return False, 'Este cupón ha expirado'
        if self.usage_limit and self.times_used >= self.usage_limit:
            return False, 'Este cupón ha alcanzado su límite de usos'
        return True, 'Cupón válido'
    
    def can_be_used_by(self, user):
        """Verifica si un usuario específico puede usar este cupón"""
        is_valid, message = self.is_valid()
        if not is_valid:
            return False, message
        
        # Verificar límite por usuario
        user_usage_count = CouponUsage.objects.filter(
            coupon=self, 
            user=user
        ).count()
        
        if user_usage_count >= self.usage_limit_per_user:
            return False, f'Ya has usado este cupón el máximo de veces permitido ({self.usage_limit_per_user})'
        
        return True, 'Cupón disponible'
    
    def calculate_discount(self, subtotal):
        """Calcula el monto de descuento para un subtotal dado"""
        if self.discount_type == 'percentage':
            discount = subtotal * (self.discount_value / Decimal('100'))
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value
        
        # No puede ser mayor al subtotal
        return min(discount, subtotal)
    
    def apply_to_order(self, order):
        """Aplica el cupón a una orden"""
        can_use, message = self.can_be_used_by(order.user)
        if not can_use:
            return False, message
        
        if order.subtotal < self.min_purchase_amount:
            return False, f'Compra mínima requerida: ${self.min_purchase_amount:,.0f} COP'
        
        discount = self.calculate_discount(order.subtotal)
        order.coupon = self
        order.discount_amount = discount
        order.total_amount = order.subtotal - discount + order.shipping_cost + order.tax
        order.save()
        
        # Registrar uso
        CouponUsage.objects.create(coupon=self, user=order.user, order=order)
        self.times_used += 1
        self.save()
        
        return True, f'Cupón aplicado: -${discount:,.0f} COP'


class CouponUsage(models.Model):
    """Registro de uso de cupones por usuario"""
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-used_at']
        verbose_name = 'Uso de Cupón'
        verbose_name_plural = 'Usos de Cupones'
    
    def __str__(self):
        return f'{self.user.username} usó {self.coupon.code} el {self.used_at.strftime("%d/%m/%Y")}'