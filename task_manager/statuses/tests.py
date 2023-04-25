from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.statuses.constants import (
    DELETE_STATUS,
    REVERSE_CREATE,
    REVERSE_STATUSES,
    TEMPLATE_CREATE,
    TEMPLATE_DELETE,
    TEMPLATE_LIST,
    TEMPLATE_UPDATE,
    UPDATE_STATUS,
)
from task_manager.constants import REVERSE_LOGIN, MSG_NO_PERMISSION
from task_manager.statuses.models import Status
from task_manager.users.models import User


class TestStatus(TestCase):
    '''`Status` CRUD test cases.'''
    fixtures = ['users.json', 'statuses.json']

    def setUp(self):
        '''Fixtures setup for tests.'''
        self.fixture_user = User.objects.get(id=1)
        self.fixture_status_1 = Status.objects.get(id=1)
        self.fixture_status_2 = Status.objects.get(id=2)
        self.fixture_status_3 = Status.objects.get(id=3)
        self.valid_status_data = {'name': 'Pending'}
        self.invalid_status_data = {'name': ''}  # empty name
        self.update_status_data = {'name': 'Delayed'}

    def test_status_list(self):
        '''Tests for getting statuses's list.'''
        # GET response check without login
        response = self.client.get(REVERSE_STATUSES)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(REVERSE_STATUSES)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.fixture_status_1)
        self.assertContains(response, self.fixture_status_1)
        self.assertContains(response, self.fixture_status_1)
        self.assertTemplateUsed(response, TEMPLATE_LIST)

    def test_status_create(self):
        '''Tests for statuses's creation.'''
        # GET response check without login
        response = self.client.get(REVERSE_CREATE)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(REVERSE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_CREATE)

        # Valid POST response check
        response = self.client.post(REVERSE_CREATE, data=self.valid_status_data)
        self.assertRedirects(response, REVERSE_STATUSES, HTTPStatus.FOUND)
        self.assertTrue(Status.objects.filter(name='Pending').exists())

        # Invalid POST reponse check: name is empty
        response = self.client.post(REVERSE_CREATE, data=self.invalid_status_data)
        self.assertIn('name', response.context['form'].errors)
        self.assertContains(response, 'Обязательное поле.')

    def test_status_update(self):
        '''Tests for status's update.'''
        URL_PATH = reverse_lazy(UPDATE_STATUS, kwargs={'pk': self.fixture_status_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_LOGIN)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        get_reponse_with_login = self.client.get(URL_PATH)
        self.assertEqual(get_reponse_with_login.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(get_reponse_with_login, TEMPLATE_UPDATE)

        # POST response check
        response = self.client.post(URL_PATH, data=self.update_status_data)
        updated_status = Status.objects.get(id=1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_STATUSES)
        self.assertEqual(updated_status.name, self.update_status_data['name'])

    def test_status_user(self):
        '''Tests for status's delete.'''
        URL_PATH = reverse_lazy(DELETE_STATUS, kwargs={'pk': self.fixture_status_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_LOGIN)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_DELETE)

        # POST response check
        post_response = self.client.post(URL_PATH)
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(post_response, REVERSE_STATUSES)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=self.fixture_status_1.id)
