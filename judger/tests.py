from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from account.models import Account
from status import JudgeLang as JLang
from .views import JudgerProblemView, JudgerTaskView

# Create your tests here.

class JudgerProblemViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/judger/problem/{pid}'
        self.factory = APIRequestFactory()
        self.view = JudgerProblemView.as_view()
        self.auth_by = Account.objects.get(username='forcesEqual')

    def testZ_get_problem(self):
        ac_data = {
            'title': 'A+B Problem',
            'pid': 1,
            'memory_limit': 128000,
            'time_limit': 1000,
            'testdata_url': 'http://tool.gzezfisher.top/file/testdata/38qLp7_pUGiOoonaUsJ_sySUSesfx3MreUPvRpvKuTQ.zip',
        }

        request = self.factory.get(self.base_url.format(pid=ac_data['pid']))
        force_authenticate(request, self.auth_by)
        response = self.view(request, pid=ac_data['pid'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('res')
        self.assertIsNotNone(data)

        self.assertEqual(data.get('title'), ac_data['title'])
        self.assertEqual(data.get('pid'), ac_data['pid'])
        self.assertEqual(data.get('memory_limit'), ac_data['memory_limit'])
        self.assertEqual(data.get('time_limit'), ac_data['time_limit'])
        self.assertEqual(data.get('testdata_url'), ac_data['testdata_url'])
        self.assertIsNone(data.get('allow_html'))
        self.assertIsNone(data.get('enabled'))
        self.assertIsNone(data.get('tags'))
        self.assertIsNone(data.get('description'))

class JudgerTaskViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/judger/status/{tid}'
        self.factory = APIRequestFactory()
        self.view = JudgerTaskView.as_view()
        self.auth_by = Account.objects.get(username='forcesEqual')

    def testZ_get_task(self):
        ac_data = {
            'id': 3,
            'code': 'console.log("Hello World!");',
            'lang': JLang.JUDGE_LANG_JS,
            'lang_info': None,
            'problem': 2,
        }

        request = self.factory.get(self.base_url.format(tid=ac_data['id']))
        force_authenticate(request, self.auth_by)
        response = self.view(request, tid=ac_data['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('res')
        self.assertIsNotNone(data)

        self.assertEqual(data.get('id'), ac_data['id'])
        self.assertEqual(data.get('code'), ac_data['code'])
        self.assertEqual(data.get('lang'), ac_data['lang'])
        self.assertEqual(data.get('lang_info'), ac_data['lang_info'])
        self.assertEqual(data.get('problem'), ac_data['problem'])
