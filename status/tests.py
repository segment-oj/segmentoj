from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import StatusView
from account.models import Account

from . import JudgeState as JState
from . import JudgeLang as JLang

# Create your tests here.

class StatusViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/status/'
        self.factory = APIRequestFactory()
        self.view = StatusView.as_view()

    def testZ_get_status(self):
        ac_data = {
            'id': 1,
            'score': 100,
            'state': JState.JUDGE_STATUS_AC,
            'time': 100,
            'memory': 100,
            'lang': JLang.JUDGE_LANG_C,
        }

        request = self.factory.get(self.base_url)
        response = self.view(request, pid=5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('res')
        self.assertIsNotNone(data)

        self.assertEqual(data.get('id'), ac_data['id'])
        self.assertEqual(data.get('score'), ac_data['score'])
        self.assertEqual(data.get('state'), ac_data['state'])
        self.assertEqual(data.get('time'), ac_data['time'])
        self.assertEqual(data.get('memory'), ac_data['memory'])
        self.assertEqual(data.get('lang'), ac_data['lang'])
