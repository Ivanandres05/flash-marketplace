from django.test import TestCase
from .models import Cart, CartItem

class CartModelTest(TestCase):

    def setUp(self):
        self.cart = Cart.objects.create()
        self.item1 = CartItem.objects.create(cart=self.cart, product_id=1, quantity=2)
        self.item2 = CartItem.objects.create(cart=self.cart, product_id=2, quantity=1)

    def test_cart_creation(self):
        self.assertEqual(self.cart.items.count(), 2)

    def test_cart_item_quantity(self):
        self.assertEqual(self.item1.quantity, 2)
        self.assertEqual(self.item2.quantity, 1)

    def test_cart_total_price(self):
        self.item1.price = 10.00  # Assuming price is a field in CartItem
        self.item2.price = 15.00  # Assuming price is a field in CartItem
        self.assertEqual(self.cart.get_total_price(), 35.00)  # Assuming get_total_price is a method in Cart

    def test_cart_item_removal(self):
        self.cart.remove_item(self.item1)  # Assuming remove_item is a method in Cart
        self.assertEqual(self.cart.items.count(), 1)