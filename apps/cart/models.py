from django.db import models
from django.contrib.auth.models import User
from apps.catalog.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Anonymous'}"
    
    def get_total(self):
        """Calcula el total del carrito"""
        total = sum(item.product.price * item.quantity for item in self.items.all())
        return total
    
    def get_item_count(self):
        """Retorna la cantidad total de items en el carrito"""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_subtotal(self):
        """Retorna el subtotal del item (precio * cantidad)"""
        return self.product.price * self.quantity