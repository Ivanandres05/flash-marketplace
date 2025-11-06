from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class SellerProfile(models.Model):
    """Perfil de vendedor - extiende User para habilitar venta de productos"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=200, verbose_name="Nombre de la tienda")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Descripción de la tienda", blank=True)
    logo = models.ImageField(upload_to='sellers/logos/', blank=True, null=True)
    
    # Información de contacto
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Estado y verificación
    is_verified = models.BooleanField(default=False, verbose_name="Verificado")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    # Métricas
    total_sales = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    # Comisión (porcentaje que se lleva Flash)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0, 
                                         verbose_name="Comisión (%)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Perfil de Vendedor"
        verbose_name_plural = "Perfiles de Vendedores"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.store_name} (@{self.user.username})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.store_name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/vendedor/{self.slug}/"
