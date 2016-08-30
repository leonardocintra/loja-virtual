from django import forms


class ContactForm(forms.Form):
    name = forms.CharField('Nome', max_length=200)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Mensagem', widget=forms.Textarea)
    