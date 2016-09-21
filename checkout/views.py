from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, TemplateView
from django.forms import modelform_factory
from django.contrib import messages

from catalog.models import Product
from .models import CartItem



class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        # cria uma session key caso não tiver ainda
        if self.request.session.session_key is None:
            self.request.session.save()
        cart_item, created = CartItem.objects.add_item(self.request.session.session_key, product)

        print(self.request.session)

        if created:
            messages.success(self.request, 'Produto adicionado com sucesso!')
        else:
            messages.success(self.request, 'Quantidade do produto atualizado com sucesso!')
        return product.get_absolute_url()


class CartItemView(TemplateView):
    template_name = 'checkout/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        CartItemFormSet = modelform_factory(
            CartItem, fields=('quantity', ) can_delete=True, extra=0
        )
        session_key = self.request.session.session_key
        if session_key:
            context['formset'] = CartItemFormSet(queryset=CartItem.objects.filter(cart_ket=session_key))
        else:
            context['formset'] = CartItemFormSet(queryset=CartItem.objects.none())
        return context
         


create_cartitem = CreateCartItemView.as_view()