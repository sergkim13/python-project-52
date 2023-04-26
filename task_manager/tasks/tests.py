from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.constants import REVERSE_LOGIN
from task_manager.tasks.constants import (
    DELETE_TASK,
    DETAIL_TASK,
    MSG_NOT_AUTHOR_FOR_DELETE_TASK,
    REVERSE_CREATE,
    REVERSE_TASKS,
    TEMPLATE_CREATE,
    TEMPLATE_DELETE,
    TEMPLATE_DETAIL,
    TEMPLATE_LIST,
    TEMPLATE_UPDATE,
    UPDATE_TASK,
)
from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.utils import disable_rollbar


@disable_rollbar()
class TestTask(TestCase):
    '''`Task` CRUD test cases.'''
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        '''Fixtures setup for tests.'''
        self.fixture_user = User.objects.get(id=1)
        self.fixture_task_1 = Task.objects.get(id=1)
        self.fixture_task_2 = Task.objects.get(id=2)
        self.fixture_task_3 = Task.objects.get(id=3)
        self.valid_task_data = {
            'name': 'Buy a milk',
            'status': 1,
            'description': 'Buy a mlik 3,5%.',
            'executor': 1,
        }
        self.invalid_task_data_1 = {
            'name': '',  # empty name
            'status': 1,
            'description': 'Some description.',
            'executor': 1,
        }
        self.invalid_task_data_2 = {
            'name': 'Some name',
            'status': '',   # empty status
            'description': 'Some description.',
            'executor': 1,
        }
        self.update_task_data = {
            'name': 'Some updated name',
            'status': 1,
            'description': 'Some description.',
            'executor': 1,
        }

    def test_task_detail(self):
        '''Tests for getting specific task info.'''
        URL_PATH = reverse_lazy(DETAIL_TASK, kwargs={'pk': self.fixture_task_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.fixture_task_1)
        self.assertTemplateUsed(response, TEMPLATE_DETAIL)

    def test_task_list(self):
        '''Tests for getting task's list.'''
        # GET response check without login
        response = self.client.get(REVERSE_TASKS)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(REVERSE_TASKS)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.fixture_task_1)
        self.assertContains(response, self.fixture_task_2)
        self.assertContains(response, self.fixture_task_3)
        self.assertTemplateUsed(response, TEMPLATE_LIST)

    def test_task_create(self):
        '''Tests for task's creation.'''
        # GET response check without login
        response = self.client.get(REVERSE_CREATE)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(REVERSE_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_CREATE)

        # # Valid POST response check
        response = self.client.post(REVERSE_CREATE, data=self.valid_task_data)
        self.assertRedirects(response, REVERSE_TASKS, HTTPStatus.FOUND)
        self.assertTrue(Task.objects.filter(id=4).exists())
        self.assertEqual(Task.objects.get(id=4).name, self.valid_task_data['name'])

        # Invalid POST reponse check: name is empty
        response = self.client.post(REVERSE_CREATE, data=self.invalid_task_data_1)
        self.assertIn('name', response.context['form'].errors)
        self.assertContains(response, 'Обязательное поле.')

        # Invalid POST reponse check: status is empty
        response = self.client.post(REVERSE_CREATE, data=self.invalid_task_data_2)
        self.assertIn('status', response.context['form'].errors)
        self.assertContains(response, 'Обязательное поле.')

    def test_task_update(self):
        '''Tests for task's update.'''
        URL_PATH = reverse_lazy(UPDATE_TASK, kwargs={'pk': self.fixture_task_1.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(URL_PATH)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, TEMPLATE_UPDATE)

        # POST response check
        response = self.client.post(URL_PATH, data=self.update_task_data)
        updated_task = Task.objects.get(id=1)
        self.assertRedirects(response, REVERSE_TASKS, HTTPStatus.FOUND)
        self.assertEqual(updated_task.name, self.update_task_data['name'])
        self.assertEqual(updated_task.description, self.update_task_data['description'])
        self.assertEqual(updated_task.status.id, self.update_task_data['status'])
        self.assertEqual(updated_task.executor.id, self.update_task_data['executor'])

    def test_task_delete(self):
        '''Tests for task's delete.'''
        URL_PATH = reverse_lazy(DELETE_TASK, kwargs={'pk': self.fixture_task_1.id})

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
        self.assertRedirects(response, REVERSE_TASKS, HTTPStatus.FOUND)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.fixture_task_1.id)

    def test_task_delete_another_user_task(self):
        '''Tests for task's delete by not author'''
        URL_PATH = reverse_lazy(DELETE_TASK, kwargs={'pk': self.fixture_task_2.id})

        # GET response check without login
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_LOGIN, HTTPStatus.FOUND)

        # GET response check with login
        self.client.force_login(self.fixture_user)
        response = self.client.get(URL_PATH)
        self.assertRedirects(response, REVERSE_TASKS, HTTPStatus.FOUND)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, REVERSE_TASKS, HTTPStatus.FOUND)
        self.assertEqual(str(messages[0]), MSG_NOT_AUTHOR_FOR_DELETE_TASK)

        # POST response check
        response = self.client.post(URL_PATH)
        self.assertRedirects(response, REVERSE_TASKS, HTTPStatus.FOUND)
        messages = list(get_messages(response.wsgi_request))
        self.assertRedirects(response, REVERSE_TASKS, HTTPStatus.FOUND)
        self.assertEqual(str(messages[0]), MSG_NOT_AUTHOR_FOR_DELETE_TASK)
