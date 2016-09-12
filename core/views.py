from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.views.generic import View, TemplateView, CreateView

from .forms import ContactForm


User = get_user_model


class IndexView(TemplateView):
    template_name = 'index.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    model = User
    success_url = reverse_lazy('index')


def contact(request):
    success = False
    
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True    
    
    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)



index = IndexView.as_view()
register = RegisterView.as_view()