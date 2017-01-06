"""

    Model Checkout

    Autor: Leonardo Nascimento Cintra
    Data: 10/2016
    Description: nesse arquivo consta os dados que administra/grava informações de checkout

"""

from pagseguro import PagSeguro
from django.db import models
from django.conf import settings
from core.constants import STATUS_CHOICES
from core.constants import PAYMENT_OPTION_CHOICES
from catalog.models import Product


class CartItemManager(models.Manager):
    """ Carrinho Manager """

    def add_item(self, cart_key, product):
        """ Adiciona o item no carrinho """
        if self.filter(cart_key=cart_key, product=product).exists():
            create = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            create = True
            cart_item = CartItem.objects.create(cart_key=cart_key, product=product,
                                                price=product.price)
        return cart_item, create


class CartItem(models.Model):
    """ Model Item do Carrinho """

    cart_key = models.CharField('Chave do carrinho', max_length=40, db_index=True)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'), )

    def __str__(self):
        return '{} [{}]'.format(self.product, self.quantity)


class OrderManager(models.Manager):
    """ Pedidos Manager """

    def create_order(self, user, cart_items):
        """ gera um pedido """
        order = self.create(user=user)
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order, quantity=cart_item.quantity, product=cart_item.product,
                price=cart_item.price
            )
        return order


class Order(models.Model):
    """ Model Order """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário')
    status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)
    payment_option = models.CharField('Opção de pagamento', choices=PAYMENT_OPTION_CHOICES,
                                      max_length=20, default='deposito')
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = OrderManager()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido #{}'.format(self.pk)

    def products(self):
        """ retorna a lista de produtos """
        products_ids = self.items.values_list('product')
        return Product.objects.filter(pk__in=products_ids)

    def total(self):
        """ get Total da compra """
        aggregate_queryset = self.items.aggregate(
            total=models.Sum(
                models.F('price') * models.F('quantity'),
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']

    def pagseguro_update_status(self, status):
        """ Altera o status do pedido conforme o DE/PARA do status do PagSeguro """
        if status == '3':
            self.status = 1
        elif status == '7':
            self.status = 2
        self.save()

    def complete(self):
        """ Alterar o status para completo (sucesso) """
        self.status = 1
        self.save()

    def pagseguro(self):
        """ Monta os objetos do PagSeguro """
        self.payment_option = 'pagseguro'
        self.save()
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        pg.sender = {
            'email': self.user.email
        }
        pg.reference_prefix = ''
        pg.shipping = None
        pg.reference = self.pk
        for item in self.items.all():
            pg.items.append(
                {
                    'id': item.product.pk,
                    'description': item.product.name,
                    'quantity': item.quantity,
                    'amount': '%.2f' % item.price
                }
            )
        return pg

    def paypal(self):
        """ Monta os objetos do Paypal """
        self.payment_option = 'paypal'
        self.save()
        paypal_dict = {
            'upload': '1',
            'business': settings.PAYPAL_EMAIL,
            'invoice': self.pk,
            'cmd': '_cart',
            'currency_code': 'BRL',
            'charset': 'utf-8',
        }
        index = 1
        for item in self.items.all():
            paypal_dict['amount_{}'.format(index)] = '%.2f' % item.price
            paypal_dict['item_name_{}'.format(index)] = item.product.name
            paypal_dict['quantity_{}'.format(index)] = item.quantity
            index = index + 1
        return paypal_dict


class OrderItem(models.Model):
    """ Model Item do pedido """

    order = models.ForeignKey(Order, verbose_name='Pedido', related_name='items')
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens dos pedidos'

    def __str__(self):
        return '[#{}] - {}'.format(self.order.pk, self.product)




# Signals
def post_save_cart_item(instance, **kwargs):
    """ Apos salvar o carrinho de compras faz as ações abaixo """

    if instance.quantity < 1:
        instance.delete()


models.signals.post_save.connect(
    post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item'
)