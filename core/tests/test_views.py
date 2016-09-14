from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.conf import settings
from model_mommy import mommy

User = get_user_model()


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
    
    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')


class ContactViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')
    
    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'contact.html')
    
    def test_form(self):
        data = {'name': '', 'message': '', 'email': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'name', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_form_ok(self):
        data = {'name': 'test', 'message': 'test', 'email': 'test@teste.com'}
        response = self.client.post(self.url, data)
        self.assertTrue(response.context['success'])
        self.assertEqual(len(mail.outbox), 1) # outbox = caixa de saida 
        self.assertEqual(mail.outbox[0].subject, 'Contato do Django Ecommerce')


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()
    
    def tearDown(self):
        self.user.delete()

    def test_login_ok(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        data = {'username': self.user.username, 'password': '123'}
        response = self.client.post(self.login_url, data)
        redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, redirect_url)
    
    def test_user_login(self):
        response = self.client.get(self.login_url)
        self.assertTrue(not response.wsgi_request.user.is_authenticated())
        data = {'username': self.user.username, 'password': '123'}
        response = self.client.post(self.login_url, data)
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    
    def test_login_error(self):
        data = {'username': self.user.username, 'password': '456'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        error_msg = ('Por favor, entre com um Apelido / Usuario  e senha corretos.'
        ' Note que ambos os campos diferenciam maiúsculas e minúsculas.')
        self.assertFormError(response, 'form', None, error_msg)