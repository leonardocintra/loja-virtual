"""
    **** View - Catalog ****
    Description:
    Author: Leonardo Nascimento Cintra
    Created: Out/2016
"""

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db import models
from django.views.decorators.cache import cache_page

from watson import search as watson

from .models import Product, Category


class ProductListView(generic.ListView):
    
    template_name = 'catalog/product_list.html'
    context_object_name = 'product_list'
    paginate_by = 3

    def get_queryset(self):
        queryset = Product.objects.all()
        q = self.request.GET.get('q', '')
        if q:
            """ 
            esse é o jeito mais simples de fazer uma busca
            porem nao funciona certos recursos.
            A melhor forma é usar uma lib chamada watson 
            https://github.com/etianen/django-watson/wiki

            queryset = queryset.filter(
                models.Q(name__icontains=q) | 
                models.Q(category__name__icontains=q) |
                models.Q(description__icontains=q)
            )
            """
            
            queryset = watson.filter(
                queryset, q
            )

        return queryset


class CategoryListView(generic.ListView):
    template_name = 'catalog/category.html'
    context_object_name = 'product_list'
    paginate_by = 3

    def get_queryset(self):    
        return Product.objects.filter(category__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['current_category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context


@cache_page(60)
def product(request, slug):
    """ product: mostra os produtos com cache de 60 segundos """
    product = Product.objects.get(slug=slug)
    context = {
        'product': product
    }
    return render(request, 'catalog/product.html', context)


product_list = ProductListView.as_view()
category = CategoryListView.as_view()