from http import HTTPStatus
from django.test import TestCase
from task_manager.users.models import User
from task_manager.users.constants import UPDATE_USER, DELETE_USER, \
    TEMPLATE_CREATE, TEMPLATE_LIST, TEMPLATE_UPDATE, TEMPLATE_DELETE, \
    REVERSE_USERS, REVERSE_CREATE, REVERSE_LOGIN

class TestUsers(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.fixture_users = User.objects.all()
        self.fixture_user_1 = User.objects.get(id=1)
        self.fixture_user_2 = User.objects.get(id=2)
        self.fixture_user_3 = User.objects.get(id=3)
        self.valid_user_data = {
            "username": "john_kras",
            "first_name": "John",
            "last_name": "Krasinski",
            "password1": "passWORD45",
            "password2": "passWORD45",
        }

    def test_users_list(self):
        response = self.client.get(REVERSE_USERS)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertContains(response, self.fixture_user_1.username)
        self.assertContains(response, self.fixture_user_2.username)
        self.assertContains(response, self.fixture_user_3.username)

    def test_user_create(self):
        response = self.client.post(REVERSE_CREATE, data=self.valid_user_data)
        print('КОД', response)
        self.assertTrue(User.objects.get(id=4))
        # self.assertTrue(User.objects.filter(username='john_kras').exists())
        self.assertRedirects(response, REVERSE_LOGIN)
