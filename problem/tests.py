from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Problem
from .views import ProblemView, ProblemDescriptionView, ProblemTestdataView, TagView, TagListView
from account.models import Account

# Create your tests here.


class ProblemViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/problem/'
        self.factory = APIRequestFactory()
        self.view = ProblemView.as_view()

    def testZ_get_problem(self):
        ac_data = {
            'title': 'Large PID',
            'pid': 1001,
            'allow_html': False,
            'enabled': True,
            'tags': [1, 2, 3, 5],
            'memory_limit': 128000,
            'time_limit': 1000
        }

        request = self.factory.get(self.base_url)
        response = self.view(request, pid=ac_data['pid'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('res')
        self.assertIsNotNone(data)

        self.assertEqual(data.get('title'), ac_data['title'])
        self.assertEqual(data.get('pid'), ac_data['pid'])
        self.assertEqual(data.get('allow_html'), ac_data['allow_html'])
        self.assertEqual(data.get('enabled'), ac_data['enabled'])
        self.assertEqual(data.get('tags'), ac_data['tags'])
        self.assertEqual(data.get('memory_limit'), ac_data['memory_limit'])
        self.assertEqual(data.get('time_limit'), ac_data['time_limit'])

    def testX_post_new_problem(self):
        request_data = {
            'title': 'Simple Problem (new)',
            'description': 'This is the description.',
            'pid': 7,
            'allow_html': False,
            'enabled': True,
            'tags': [1, 2, 3],
        }

        request = self.factory.post(self.base_url, data=request_data)
        force_authenticate(request, Account.objects.get(username='admin'))
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testW_change_problem(self):
        request_data = {
            'title': 'Not Hard Problem',
            'description': 'This is description.',
            'pid': 8,
            'allow_html': True,
            'tags': [4, 3, 1]
        }

        ac_data = {
            'enabled': True
        }

        request = self.factory.patch(self.base_url, data=request_data)
        force_authenticate(request, Account.objects.get(username='admin'))
        response = self.view(request, pid=2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        target = Problem.objects.get(pid=request_data['pid'])
        self.assertEqual(target.pid, request_data['pid'])
        self.assertEqual(target.description, request_data['description'])
        self.assertEqual(target.title, request_data['title'])
        self.assertEqual(target.allow_html, request_data['allow_html'])
        self.assertEqual(target.enabled, ac_data['enabled'])


class ProblemDescriptionViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/problem/{pid}/description'
        self.factory = APIRequestFactory()
        self.view = ProblemDescriptionView.as_view()

    def testZ_get_problem_description(self):
        ac_data = {
            'description': 'Large PID Problem Test'
        }

        request = self.factory.get(self.base_url.format(pid=1001))
        response = self.view(request, pid=1001)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('res')
        self.assertIsNotNone(data)
        self.assertEqual(data.get('description'), ac_data['description'])


class ProblemTestdataViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/problem/{pid}/testdata'
        self.factory = APIRequestFactory()
        self.view = ProblemTestdataView.as_view()

    def testZ_get_problem_testdata_url(self):
        ac_data = {
            'testdata_url': 'http://tool.gzezfisher.top/file/testdata/38qLp7_pUGiOoonaUsJ_sySUSesfx3MreUPvRpvKuTQ.zip'
        }

        request = self.factory.get(self.base_url.format(pid=1))
        force_authenticate(request, Account.objects.get(username='admin'))
        response = self.view(request, pid=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('res')
        self.assertIsNotNone(data)
        self.assertEqual(data, ac_data['testdata_url'])

    def testY_set_problem_testdata_url(self):
        request_data = {
            'testdata_url': 'https://example.com'
        }

        target = Problem.objects.get(pid=1001)
        request = self.factory.patch(self.base_url.format(pid=target.pid), data=request_data)
        force_authenticate(request, Account.objects.get(username='admin'))
        response = self.view(request, pid=target.pid)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        target = Problem.objects.get(pid=1001)
        self.assertEqual(target.testdata_url, request_data['testdata_url'])


class TagViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/problem/tag'
        self.factory = APIRequestFactory()
        self.view = TagView.as_view()

    def testZ_get_tag(self):
        ac_data = {
            'id': 1,
            'content': 'hard',
            'color': 'blue',
        }

        request = self.factory.get(self.base_url)
        response = self.view(request, tid=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('res')
        self.assertIsNotNone(data)

        self.assertEqual(data.get('id'), ac_data['id'])
        self.assertEqual(data.get('content'), ac_data['content'])
        self.assertEqual(data.get('color'), ac_data['color'])


class TagListViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/problem/tag/list'
        self.factory = APIRequestFactory()
        self.view = TagListView.as_view()

    def testA_get_list(self):
        request = self.factory.get(self.base_url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
