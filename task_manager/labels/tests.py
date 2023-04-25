from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.constants import REVERSE_LOGIN
from task_manager.labels.constants import (
    DELETE_LABEL,
    LABEL_USED_IN_TASK,
    REVERSE_CREATE,
    REVERSE_LABELS,
    TEMPLATE_CREATE,
    TEMPLATE_DELETE,
    TEMPLATE_LIST,
    TEMPLATE_UPDATE,
    UPDATE_LABEL,
)
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TestLabel(TestCase):
    '''`Label` CRUD test cases.'''
    fixtures = ['users.json', 'labels.json']

    def setUp(self):
        '''Fixtures setup for tests.'''
        self.fixture_user = User.objects.get(id=1)
        self.fixture_label_1 = Label.objects.get(id=1)
        self.fixture_label_2 = Label.objects.get(id=2)
        self.fixture_label_3 = Label.objects.get(id=3)
        self.valid_label_data = {'name': 'DevOps'}
        self.invalid_label_data = {'name': ''}  # empty name
        self.update_label_data = {'name': 'IT'}

    def test_label_list(self):
        '''Tests for getting label's list.'''
        # GET response check without login
        response = self.client.get(REVERSE_LABELS)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(REVERSE_LABELS)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.fixture_label_1)
        self.assertContains(response, self.fixture_label_1)
        self.assertContains(response, self.fixture_label_1)
        self.assertTemplateUsed(response, TEMPLATE_LIST)

    def test_label_create(self):
        '''Tests for labels's creation.'''
        # GET response check without login
        response = self.client.get(REVERSE_CREATE)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(REVERSE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_CREATE)

        # Valid POST response check
        response = self.client.post(REVERSE_CREATE, data=self.valid_label_data)
        self.assertRedirects(response, REVERSE_LABELS, HTTPStatus.FOUND)
        self.assertTrue(Label.objects.filter(name=self.valid_label_data['name']).exists())

        # Invalid POST reponse check: name is empty
        response = self.client.post(REVERSE_CREATE, data=self.invalid_label_data)
        self.assertIn('name', response.context['form'].errors)
        self.assertContains(response, 'Обязательное поле.')

    def test_label_update(self):
        '''Tests for label's update.'''
        URL_PATH = reverse_lazy(UPDATE_LABEL, kwargs={'pk': self.fixture_label_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_UPDATE)

        # POST response check
        response = self.client.post(URL_PATH, data=self.update_label_data)
        updated_label = Label.objects.get(id=1)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, REVERSE_LABELS)
        self.assertEqual(updated_label.name, self.update_label_data['name'])

    def test_label_delete(self):
        '''Tests for label's delete.'''
        URL_PATH = reverse_lazy(DELETE_LABEL, kwargs={'pk': self.fixture_label_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_DELETE)

        # POST response check
        response = self.client.post(URL_PATH)
        self.assertRedirects(response, REVERSE_LABELS, HTTPStatus.FOUND)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(id=self.fixture_label_1.id)


class TestLabelRelations(TestCase):
    '''`Label` test cases with related `Task`'''
    fixtures = ['users.json', 'labels.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        '''Fixtures setup for tests.'''
        self.fixture_user = User.objects.get(id=1)
        self.fixture_label_1 = Label.objects.get(id=1)
        fixture_task = Task.objects.get(id=1)
        fixture_task.labels.add(self.fixture_label_1)

    def test_label_with_task_delete(self):
        '''Tests for label's delete which used in task.'''
        URL_PATH = reverse_lazy(DELETE_LABEL, kwargs={'pk': self.fixture_label_1.id})
        self.client.force_login(self.fixture_user)
        response = self.client.post(URL_PATH)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, REVERSE_LABELS, HTTPStatus.FOUND)
        self.assertEqual(str(messages[0]), LABEL_USED_IN_TASK)
