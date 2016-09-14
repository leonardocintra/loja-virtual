from django.shortcuts import render
from django.views.generic import CreateView

from .models import User
from .forms import UserAdminCreationForm


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = UserAdminCreationForm


register = RegisterView.as_view()