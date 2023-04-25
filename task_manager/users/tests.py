from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.constants import REVERSE_LOGIN
from task_manager.users.constants import (
    DELETE_USER,
    REVERSE_CREATE,
    REVERSE_USERS,
    TEMPLATE_CREATE,
    TEMPLATE_DELETE,
    TEMPLATE_LIST,
    TEMPLATE_UPDATE,
    UPDATE_USER,
    USER_USED_IN_TASK,
)
from task_manager.users.models import User


class TestUser(TestCase):
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

        # GET response check
        response = self.client.get(REVERSE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_CREATE)

        # Valid POST response check
        response = self.client.post(REVERSE_CREATE, data=self.valid_user_data)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(username='john_kras').exists())

        # Invalid POST reponse check: username contains space
        invalid_post_response_1 = self.client.post(REVERSE_CREATE, data=self.invalid_user_data_1)
        self.assertIn('username', invalid_post_response_1.context['form'].errors)
        self.assertContains(
            invalid_post_response_1,
            'Введите правильное имя пользователя. Оно может содержать только буквы, цифры и знаки'
        )

        # Invalid POST reponse check: firstname is empty
        response = self.client.post(REVERSE_CREATE, data=self.invalid_user_data_2)
        self.assertIn('first_name', response.context['form'].errors)
        self.assertContains(response, 'Обязательное поле.')

        # Invalid POST reponse check: firstname is too long
        response = self.client.post(REVERSE_CREATE, data=self.invalid_user_data_3)
        self.assertIn('first_name', response.context['form'].errors)
        self.assertContains(response, 'Убедитесь, что это значение содержит не более 150 символов (сейчас 200).')

        # Invalid POST reponse check: passwords do not match
        response = self.client.post(REVERSE_CREATE, data=self.invalid_user_data_4)
        self.assertIn('password2', response.context['form'].errors)
        self.assertContains(response, 'Введенные пароли не совпадают.')

        # Invalid POST response check: duplicate username
        response = self.client.post(REVERSE_CREATE, data=self.valid_user_data)
        self.assertIn('username', response.context['form'].errors)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')

    def test_user_update(self):
        '''Tests for user's update.'''
        URL_PATH = reverse_lazy(UPDATE_USER, kwargs={'pk': self.fixture_user_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user_1)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_UPDATE)

        # POST response check
        response = self.client.post(URL_PATH, data=self.update_user_data)
        updated_user = User.objects.get(id=1)
        self.assertRedirects(response, REVERSE_USERS, HTTPStatus.FOUND)
        self.assertEqual(updated_user.username, self.update_user_data['username'])
        self.assertEqual(updated_user.first_name, self.update_user_data['first_name'])
        self.assertEqual(updated_user.last_name, self.update_user_data['last_name'])

    def test_user_update_not_self(self):
        '''Tests for user's update other user.'''
        URL_PATH = reverse_lazy(UPDATE_USER, kwargs={'pk': self.fixture_user_2.id})

        # GET response check
        self.client.force_login(self.fixture_user_1)
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_USERS, HTTPStatus.FOUND)

        # POST response check
        response = self.client.post(URL_PATH)
        self.assertRedirects(response, REVERSE_USERS, HTTPStatus.FOUND)

    def test_user_delete(self):
        '''Tests for users's delete.'''
        URL_PATH = reverse_lazy(DELETE_USER, kwargs={'pk': self.fixture_user_1.id})

        # GET response check
        self.client.force_login(self.fixture_user_1)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_DELETE)

        # POST response check
        response = self.client.post(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_USERS)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.fixture_user_1.id)

    def test_user_delete_not_self(self):
        '''Tests for user's delete other user.'''
        URL_PATH = reverse_lazy(DELETE_USER, kwargs={'pk': self.fixture_user_2.id})

        # GET response check
        self.client.force_login(self.fixture_user_1)
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_USERS, HTTPStatus.FOUND)

        # POST response check
        response = self.client.post(URL_PATH)
        self.assertRedirects(response, REVERSE_USERS, HTTPStatus.FOUND)


class TestUserRelations(TestCase):
    '''`User` test cases with related `Task`'''
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        '''Fixtures setup for tests.'''
        self.fixture_user = User.objects.get(id=1)

    def test_status_with_task_delete(self):
        '''Tests for users's delete which assigned as executor in task.'''
        URL_PATH = reverse_lazy(DELETE_USER, kwargs={'pk': self.fixture_user.id})
        self.client.force_login(self.fixture_user)
        response = self.client.post(URL_PATH)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, REVERSE_USERS, HTTPStatus.FOUND)
        self.assertEqual(str(messages[0]), USER_USED_IN_TASK)
