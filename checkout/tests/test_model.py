from django.test import Client, TestCase
from model_mommy import mommy

from checkout.models import CartItem


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