from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from model_mommy import mommy
from accounts.models import User



class RegisterViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
    
    def test_register_ok(self):
        data = {
            'username': 'leonardo', 
            'password1': 'MagazineLuiza123!@#', 
            'password2': 'MagazineLuiza123!@#',
            'email': 'test@teste.com'
        }
        response = self.client.post(self.register_url, data)
        index_url = reverse('index')
        self.assertRedirects(response, index_url)
        self.assertEqual(User.objects.count(), 1)
    
    def test_register_error(self):
        data = {'username': 'leonardo', 'password1': 'MagazineLuiza123!@#', 'password2': 'MagazineLuiza123!@#'}
        response = self.client.post(self.register_url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')

    
class UpdateUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:update_user')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_update_user_ok(self):
        data = {'name': 'User Teste', 'email': 'teste@testinho.com'}
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        accounts_index_url = reverse('accounts:index')
        self.assertRedirects(response, accounts_index_url)
        user = User.objects.get(username=self.user.username)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'teste@testinho.com')
        self.assertEqual(self.user.name, 'User Teste')

    def test_update_user_error(self):
        data = {}
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
    

class UpdatePasswordTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:update_password')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()


    def tearDown(self):
        self.user.delete()

    def test_update_password_ok(self):
        # tem que olhar na documentação do Django o PasswordChangeForm (views.py)
        data = {'old_password': '123', 'new_password1': 'MagazineLuiza123!@#', 'new_password2': 'MagazineLuiza123!@#'}
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('MagazineLuiza123!@#'))
