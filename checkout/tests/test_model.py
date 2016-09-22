from django.test import Client, TestCase
from django.conf import settings
from model_mommy import mommy

from checkout.models import CartItem, Order


class CartItemTestCase(TestCase):
    def setUp(self):
         mommy.make(CartItem, _quantity=3)
    
    def tearDown(self):
        pass
    
    def test_post_save_cart_item(self):
        cart_item = CartItem.objects.all()[0]
        cart_item.quantity = 0
        cart_item.save()
        self.assertEqual(CartItem.objects.count(), 2)


class OrderTestCase(TestCase):
    def setUp(self):
        self.cart_item = mommy.make(CartItem)
        self.user = mommy.make(settings.AUTH_USER_MODEL)
    
    def tearDown(self):
        pass
    
    def test_create_order(self):
        Order.objects.create_order(self.user, [self.cart_item])
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEqual(order.user, self.user)
        order_item = order.items.get() # items = related_name do model Order
        self.assertEqual(order_item.product, self.cart_item.product)
    
