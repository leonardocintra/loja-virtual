from django.conf.urls import url
from django.contrib import admin
from core import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^contato/$', views.contact, name='contact'),
    url(r'^produto/$', views.product, name='product'),
    url(r'^produtos/$', views.product_list, name='product_list'),

    url(r'^admin/', admin.site.urls),
]
