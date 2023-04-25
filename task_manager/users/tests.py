from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.users.constants import (
    DELETE_USER,
    REVERSE_CREATE,
    REVERSE_USERS,
    TEMPLATE_CREATE,
    TEMPLATE_DELETE,
    TEMPLATE_LIST,
    TEMPLATE_UPDATE,
    UPDATE_USER,
)
from task_manager.constants import REVERSE_LOGIN
from task_manager.users.models import User


class TestUsers(TestCase):
    '''`User` CRUD test cases.'''
    fixtures = ['users.json']

    def setUp(self):
        '''Fixtures setup for tests.'''
        self.fixture_user_1 = User.objects.get(id=1)
        self.fixture_user_2 = User.objects.get(id=2)
        self.fixture_user_3 = User.objects.get(id=3)
        self.valid_user_data = {
            'username': 'john_kras',
            'first_name': 'John',
            'last_name': 'Krasinski',
            'password1': 'asdasd=fassafdasf',
            'password2': 'asdasd=fassafdasf',
        }
        self.invalid_user_data_1 = {
            'username': 'john kras',  # contains spaces
            'first_name': 'John',
            'last_name': 'Krasinski',
            'password1': 'asdasd=fassafdasf',
            'password2': 'asdasd=fassafdasf',
        }
        self.invalid_user_data_2 = {
            'username': 'john_kras1',
            'first_name': '',  # empty first_name
            'last_name': 'Krasinski',
            'password1': 'asdasd=fassafdasf',
            'password2': 'asdasd=fassafdasf',
        }
        self.invalid_user_data_3 = {
            'username': 'john_kras1',
            'first_name': f"{'John' * 50}",  # too long first_name
            'last_name': 'Krasinski',
            'password1': 'asdasd=fassafdasf',
            'password2': 'asdasd=fassafdasf',
        }
        self.invalid_user_data_4 = {
            'username': 'john_kras1',
            'first_name': 'John',
            'last_name': 'Krasinski',
            'password1': 'asdasd=fassafdasf',
            'password2': 'asdasd=fassafdasf1',  # passwords do not match
        }
        self.update_user_data = {
            'username': 'john_krasinki7',  # update username
            'first_name': 'John',
            'last_name': 'Krasinski',
            'password1': 'asdasd=fassafdasf',
            'password2': 'asdasd=fassafdasf',
        }

    def test_users_list(self):
        '''Tests for getting user's list.'''
        response = self.client.get(REVERSE_USERS)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.fixture_user_1.username)
        self.assertContains(response, self.fixture_user_2.username)
        self.assertContains(response, self.fixture_user_3.username)
        self.assertTemplateUsed(response, TEMPLATE_LIST)

    def test_user_create(self):
        '''Tests for user's creation.'''
        valid_get_response = self.client.get(REVERSE_CREATE)
        valid_post_response = self.client.post(REVERSE_CREATE, data=self.valid_user_data)
        invalid_post_response_1 = self.client.post(REVERSE_CREATE, data=self.invalid_user_data_1)
        invalid_post_response_2 = self.client.post(REVERSE_CREATE, data=self.invalid_user_data_2)
        invalid_post_response_3 = self.client.post(REVERSE_CREATE, data=self.invalid_user_data_3)
        invalid_post_response_4 = self.client.post(REVERSE_CREATE, data=self.invalid_user_data_4)
        invalid_post_response_5 = self.client.post(REVERSE_CREATE, data=self.valid_user_data)

        # Valid GET response check
        self.assertEqual(valid_get_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(valid_get_response, TEMPLATE_CREATE)

        # Valid POST response check
        self.assertEqual(valid_post_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(valid_post_response, REVERSE_LOGIN)
        self.assertTrue(User.objects.filter(username='john_kras').exists())

        # Invalid POST reponse check: username contains space
        self.assertIn('username', invalid_post_response_1.context['form'].errors)
        self.assertContains(
            invalid_post_response_1,
            'Введите правильное имя пользователя. Оно может содержать только буквы, цифры и знаки'
        )

        # Invalid POST reponse check: firstname is empty
        self.assertIn('first_name', invalid_post_response_2.context['form'].errors)
        self.assertContains(invalid_post_response_2, 'Обязательное поле.')

        # Invalid POST reponse check: firstname is too long
        self.assertIn('first_name', invalid_post_response_3.context['form'].errors)
        self.assertContains(
            invalid_post_response_3,
            'Убедитесь, что это значение содержит не более 150 символов (сейчас 200).'
        )

        # Invalid POST reponse check: passwords do not match
        self.assertIn('password2', invalid_post_response_4.context['form'].errors)
        self.assertContains(invalid_post_response_4, 'Введенные пароли не совпадают.')

        # Invalid POST response check: duplicate username
        self.assertIn('username', invalid_post_response_5.context['form'].errors)
        self.assertContains(invalid_post_response_5, 'Пользователь с таким именем уже существует.')

    def test_user_update(self):
        '''Tests for user's update.'''
        URL_PATH = reverse_lazy(UPDATE_USER, kwargs={'pk': self.fixture_user_1.id})

        # GET response check without login
        get_reponse_without_login = self.client.get(URL_PATH)
        self.assertEqual(get_reponse_without_login.status_code, HTTPStatus.FOUND)
        self.assertRedirects(get_reponse_without_login, reverse_lazy('users'))

        # GET response check with login
        self.client.force_login(self.fixture_user_1)
        get_reponse_with_login = self.client.get(URL_PATH)
        self.assertEqual(get_reponse_with_login.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(get_reponse_with_login, TEMPLATE_UPDATE)

        # POST response check
        post_response = self.client.post(URL_PATH, data=self.update_user_data)
        updated_user = User.objects.get(id=1)
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(post_response, REVERSE_USERS)
        self.assertEqual(updated_user.username, self.update_user_data['username'])
        self.assertEqual(updated_user.first_name, self.update_user_data['first_name'])
        self.assertEqual(updated_user.last_name, self.update_user_data['last_name'])

    def test_delete_user(self):
        '''Tests for users's delete.'''
        URL_PATH = reverse_lazy(DELETE_USER, kwargs={'pk': self.fixture_user_1.id})

        # GET response check
        self.client.force_login(self.fixture_user_1)
        get_reponse_with_login = self.client.get(URL_PATH)
        self.assertEqual(get_reponse_with_login.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(get_reponse_with_login, TEMPLATE_DELETE)

        # POST response check
        post_response = self.client.post(URL_PATH)
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(post_response, REVERSE_USERS)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.fixture_user_1.id)
