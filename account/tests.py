from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

import json

# Create your tests here.
class UserTest(TestCase):
    fixtures = ['testdatabase.yaml']

    # setup test case
    def setUp(self):
        self.base_url = '/api/user'
        self.client = APIClient()

    # test adding a user
    def testA_add_user(self):
        request_data = {
            'username': 'unittesuser01',
            'email': 'unittesuser01@soj.ac.cn',
            'password': 'unittest'
        }

        res = self.client.put(self.base_url, data=request_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_json = json.loads(res.content)
        self.assertEqual(type(res_json['res']['id']), int)

    def testB_get_user(self):
        user_data = {
            'id': 1,
            'username': 'admin',
            'introduction': '# Hello World!',
            'email': 'admin@soj.ac.cn',
            'lang': 0,
            'is_staff': True,
            'is_active': True,
            'is_superuser': True
        }

        res = self.client.get(self.base_url, {'id': 1})
        res_json = json.loads(res.content)
        res_data = res_json['res']
        self.assertEqual(res_data.get('id'), user_data['id'])
        self.assertEqual(res_data.get('username'), user_data['username'])
        self.assertEqual(res_data.get('introduction'), user_data['introduction'])
        self.assertEqual(res_data.get('lang'), user_data['lang'])
        self.assertEqual(res_data.get('is_staff'), user_data['is_staff'])
        self.assertEqual(res_data.get('is_active'), user_data['is_active'])
        self.assertEqual(res_data.get('is_superuser'), user_data['is_superuser'])
