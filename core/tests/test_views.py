from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail


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