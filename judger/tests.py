from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import JudgerStatusView
from account.models import User

# Create your tests here.


class JudgerStatusTest(TestCase):
    def setUp(self):
        self.base_url = "/api/judger/status"
        self.factory = APIRequestFactory()
        self.view = JudgerStatusView.as_view()

    def testA_get_task(self):
        ac_data = 3

        request = self.factory.get(self.base_url)
        force_authenticate(request, User.objects.get(username="forcesequal"))
        response = self.view(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("res")
        self.assertEqual(data, ac_data)
