from django.core.management import call_command
from django.db.models.signals import pre_save
from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser
from baskets.models import Basket
from geekshop import settings
from ordersapp.models import OrderItem


class Tests(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_data/test_users.json')
        call_command('loaddata', 'test_data/test_products.json')
        res = pre_save.disconnect(sender=Basket, dispatch_uid='basket_change_quantity_pre_save')
        assert res, 'can not mute Basket pre_save signal'
        call_command('loaddata', 'test_data/test_baskets.json')
        res = pre_save.disconnect(sender=OrderItem, dispatch_uid='orderitem_change_quantity_pre_save')
        assert res, 'can not mute OrderItem pre_save signal'
        call_command('loaddata', 'test_data/test_ordersapp.json')
        self.user = ShopUser.objects.create_user('someuser', 'someuser@someuser.local', 'password')
        self.client = Client()

    def test_auth_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        response = self.client.get('/auth/profile')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/auth/login?next=/auth/profile')

        self.client.login(username='someuser', password='password')
        response = self.client.get('/auth/login')
        self.assertEqual(response.context['user'], self.user)

    def test_user_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'GeekShop - Регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '21'}

        response = self.client.post('/auth/register', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 302)

        # данные нового пользователя
        self.client.login(
            username=new_user_data['username'],
            password=new_user_data['password1']
        )

        # логинимся
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(
            response,
            text=new_user_data['username'],
            status_code=200
        )

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'merypoppins@geekshop.local',
            'age': '17'}

        response = self.client.post('/auth/register', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды!')


class TestModels(TestCase):

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_data/test_users.json')
        call_command('loaddata', 'test_data/test_products.json')
        res = pre_save.disconnect(sender=Basket, dispatch_uid='basket_change_quantity_pre_save')
        assert res, 'can not mute Basket pre_save signal'
        call_command('loaddata', 'test_data/test_baskets.json')

    def test_models_method(self):
        expected_values = ('70945.10', 10)
        baskets = Basket.objects.filter(user__username='user').order_by('id')
        self.assertEqual(expected_values[0], str(baskets.first().total_sum()))
        self.assertEqual(expected_values[1], baskets.first().total_quantity())
