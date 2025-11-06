from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal


class Coupon(models.Model):
    """
    Cupones de descuento para el marketplace
    """
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Porcentaje'),
        ('fixed', 'Monto Fijo'),
    ]
    
    code = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name='Código del Cupón',
        help_text='Ej: FLASH10, PRIMERACOMPRA, VERANO2025'
    )
    name = models.CharField(max_length=200, verbose_name='Nombre del Cupón')
    description = models.TextField(blank=True, verbose_name='Descripción')
    
    # Tipo de descuento
    discount_type = models.CharField(
        max_length=10, 
        choices=DISCOUNT_TYPE_CHOICES, 
        default='percentage',
        verbose_name='Tipo de Descuento'
    )
    discount_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor del Descuento',
        help_text='Porcentaje (1-100) o monto fijo en COP'
    )
    
    # Validez temporal
    valid_from = models.DateTimeField(verbose_name='Válido Desde')
    valid_to = models.DateTimeField(verbose_name='Válido Hasta')
    
    # Límites de uso
    usage_limit = models.PositiveIntegerField(
        null=True, 
        blank=True,
        verbose_name='Límite de Usos Total',
        help_text='Dejar en blanco para ilimitado'
    )
    usage_limit_per_user = models.PositiveIntegerField(
        default=1,
        verbose_name='Límite de Usos por Usuario',
        help_text='Cuántas veces puede usar el cupón cada usuario'
    )
    times_used = models.PositiveIntegerField(default=0, verbose_name='Veces Usado')
    
    # Restricciones
    minimum_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Compra Mínima',
        help_text='Monto mínimo de compra para aplicar el cupón (COP)'
    )
    maximum_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Descuento Máximo',
        help_text='Descuento máximo en COP (para cupones de porcentaje)'
    )
    
    # Usuarios específicos (opcional)
    specific_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='exclusive_coupons',
        verbose_name='Usuarios Específicos',
        help_text='Dejar vacío para todos los usuarios'
    )
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_coupons',
        verbose_name='Creado por'
    )
    
    class Meta:
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.discount_type == 'percentage':
            return f"{self.code} - {self.discount_value}% OFF"
        else:
            return f"{self.code} - ${self.discount_value:,.0f} COP OFF"
    
    def is_valid(self):
        """Verificar si el cupón es válido actualmente"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_to and
            (self.usage_limit is None or self.times_used < self.usage_limit)
        )
    
    def can_be_used_by(self, user):
        """Verificar si el usuario puede usar este cupón"""
        if not self.is_valid():
            return False, "Cupón inválido o expirado"
        
        # Verificar si es para usuarios específicos
        if self.specific_users.exists() and user not in self.specific_users.all():
            return False, "Este cupón no está disponible para tu cuenta"
        
        # Verificar límite por usuario
        user_usage = CouponUsage.objects.filter(coupon=self, user=user).count()
        if user_usage >= self.usage_limit_per_user:
            return False, f"Ya has usado este cupón {self.usage_limit_per_user} vez/veces"
        
        return True, "OK"
    
    def calculate_discount(self, subtotal):
        """Calcular el descuento para un subtotal dado"""
        if self.discount_type == 'percentage':
            discount = subtotal * (self.discount_value / Decimal('100'))
            # Aplicar descuento máximo si existe
            if self.maximum_discount:
                discount = min(discount, self.maximum_discount)
        else:
            discount = self.discount_value
        
        # No puede ser mayor al subtotal
        return min(discount, subtotal)
    
    def apply_to_order(self, subtotal, user):
        """Aplicar cupón a un pedido y retornar información"""
        can_use, message = self.can_be_used_by(user)
        
        if not can_use:
            return {
                'success': False,
                'message': message,
                'discount': Decimal('0.00')
            }
        
        if subtotal < self.minimum_purchase:
            return {
                'success': False,
                'message': f'Compra mínima de ${self.minimum_purchase:,.0f} COP',
                'discount': Decimal('0.00')
            }
        
        discount = self.calculate_discount(subtotal)
        
        return {
            'success': True,
            'message': f'Cupón aplicado: {self.code}',
            'discount': discount,
            'final_total': subtotal - discount
        }


class CouponUsage(models.Model):
    """
    Registro de uso de cupones por usuarios
    """
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Descontado')
    used_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Uso')
    
    class Meta:
        verbose_name = 'Uso de Cupón'
        verbose_name_plural = 'Usos de Cupones'
        ordering = ['-used_at']
    
    def __str__(self):
        return f"{self.user.username} usó {self.coupon.code} - ${self.discount_amount:,.0f}"
