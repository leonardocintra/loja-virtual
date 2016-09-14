from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

from .forms import ContactForm


User = get_user_model


class IndexView(TemplateView):
    template_name = 'index.html'


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