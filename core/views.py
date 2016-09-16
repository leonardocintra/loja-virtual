from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.contrib import messages

from .forms import ContactForm


class IndexView(TemplateView):
    template_name = 'index.html'


def contact(request):
    success = False

    form = ContactForm(request.POST or None)
    if form.is_valid():
        form.send_mail()
        success = True
    elif request.method == 'POST':
        messages.error(request, 'Formulário Inválido')
    
    context = {
        'form': form,
        'success': success
    }
    return render(request, 'contact.html', context)



index = IndexView.as_view()