from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import JudgerStatusView
from account.models import User

# Create your tests here.


class JudgerStatusTest(TestCase):
    fixtures = ["testdatabase.yaml"]

    def setUp(self):
        self.base_url = "/api/judger/status"
        self.factory = APIRequestFactory()
        self.view = JudgerStatusView.as_view()

    def testA_get_task(self):
        ac_data = 3

        request = self.factory.get(self.base_url)
        force_authenticate(request, user=User.objects.get(username="ForcesEqual"))
        response = self.view(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("res")
        self.assertEqual(data, ac_data)

    def testB_get_task_not_logged_in(self):
        request = self.factory.get(self.base_url)
        force_authenticate(request) # Logout
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def testC_get_task_not_judger(self):
        request = self.factory.get(self.base_url)
        force_authenticate(request, user=User.objects.get(username="admin"))
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
