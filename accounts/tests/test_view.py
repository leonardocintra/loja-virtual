from django.test import Client, TestCase
from django.core.urlresolvers import reverse


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
    
    def test_register_ok(self):
        data = {'username': 'leonardo', 'password1': 'teste123', 'password2': 'teste123'}
        response = self.client.post(self.register_url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
