from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

# Comentamos el User personalizado para usar el estándar de Django
# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     def __str__(self):
#         return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Preferencias de notificaciones
    email_notifications = models.BooleanField(default=True, verbose_name="Recibir notificaciones por email")
    order_notifications = models.BooleanField(default=True, verbose_name="Notificaciones de pedidos")
    promotional_notifications = models.BooleanField(default=True, verbose_name="Notificaciones promocionales")

    def __str__(self):
        return self.user.username

class Seller(models.Model):
    """Perfil de vendedor - permite a usuarios vender productos"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=200, unique=True, verbose_name="Nombre de la tienda")
    description = models.TextField(blank=True, verbose_name="Descripción de la tienda")
    logo = models.ImageField(upload_to='sellers/logos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False, verbose_name="Vendedor verificado")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Información adicional
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Estadísticas
    total_sales = models.PositiveIntegerField(default=0, verbose_name="Ventas totales")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    
    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.store_name} (@{self.user.username})"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

class Wishlist(models.Model):
    """Lista de deseos del usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class PaymentMethod(models.Model):
    """Métodos de pago guardados del usuario"""
    CARD_TYPES = (
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
        ('other', 'Otra'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    card_type = models.CharField(max_length=20, choices=CARD_TYPES, default='visa')
    card_holder = models.CharField(max_length=200, verbose_name="Titular de la tarjeta")
    card_number = models.CharField(max_length=4, verbose_name="Últimos 4 dígitos")  # Solo guardamos los últimos 4
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=2)
    is_default = models.BooleanField(default=False, verbose_name="Tarjeta predeterminada")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.card_type.upper()} ****{self.card_number} - {self.card_holder}"
    
    def save(self, *args, **kwargs):
        # Si es la tarjeta predeterminada, quitar el default de las demás
        if self.is_default:
            PaymentMethod.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class PasswordResetCode(models.Model):
    """Códigos de recuperación de contraseña"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_codes')
    code = models.CharField(max_length=6, verbose_name="Código de verificación")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(verbose_name="Expira en")
    is_used = models.BooleanField(default=False, verbose_name="Usado")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Código de recuperación"
        verbose_name_plural = "Códigos de recuperación"
    
    def __str__(self):
        return f"{self.user.email} - {self.code}"
    
    @staticmethod
    def generate_code():
        """Genera un código de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_valid(self):
        """Verifica si el código es válido (no usado y no expirado)"""
        return not self.is_used and timezone.now() < self.expires_at
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            # El código expira en 15 minutos
            self.expires_at = timezone.now() + timezone.timedelta(minutes=15)
        super().save(*args, **kwargs)
