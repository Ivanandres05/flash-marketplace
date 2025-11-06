from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True, verbose_name="Vendedor")
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_seller_name(self):
        """Retorna el nombre de la tienda del vendedor o 'Flash' si no tiene"""
        if self.seller and hasattr(self.seller, 'seller_profile'):
            return self.seller.seller_profile.store_name
        return "Flash Marketplace"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255)

    def __str__(self):
        return f"Image for {self.product.name}"