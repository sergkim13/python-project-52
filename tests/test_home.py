from http import HTTPStatus

from django.contrib.auth import SESSION_KEY
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.constants import (
    HOME,
    REVERSE_HOME,
    REVERSE_LOGIN,
    REVERSE_LOGOUT,
    TEMPLATE_INDEX,
)
from task_manager.users.models import User
from task_manager.utils import disable_rollbar


@disable_rollbar()
class HomePageTest(TestCase):
    '''Home page test case.'''

    def test_home_page_view(self):
        '''Home page view test.'''
        URL_PATH = reverse_lazy(HOME)

        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, template_name=TEMPLATE_INDEX)


@disable_rollbar()
class AuthenticationTest(TestCase):
    '''Authentication test cases.'''
    fixtures = ['users.json']

    def setUp(self) -> None:
        '''Fixtures setup for tests.'''
        self.credentials = {
            'username': 'test_user',
            'password': 'test_pass',
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        '''Checks login process.'''
        response = self.client.post(REVERSE_LOGIN, self.credentials, follow=True)
        self.assertRedirects(response, REVERSE_HOME, HTTPStatus.FOUND)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout(self):
        '''Checks logout process.'''
        self.client.login(**self.credentials)
        self.assertTrue(SESSION_KEY in self.client.session)

        response = self.client.post(REVERSE_LOGOUT)
        self.assertTrue(SESSION_KEY not in self.client.session)
        self.assertRedirects(response, REVERSE_HOME, HTTPStatus.FOUND)
