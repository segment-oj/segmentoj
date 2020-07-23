from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import StatusView
from account.models import User 

# Create your tests here.
class StatusTest(TestCase):
    fixtures = ['testdatabase.yaml']

    # setup test case
    def setUp(self):
        self.base_url = 'api/status'
        self.view = StatusView.as_view()
    
    def testA_submit_problem(self):
        request_data = {
            'problem': 1,
            'code': '# This is the code.'
        }

        user = User.objects.get(username="testuser")

        request = APIRequestFactory.post(self.base_url, data, format='json')
        force_authenticate(request, user)
        res = self.view(request)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

