from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


from .views import ProblemView

# Create your tests here.


class ProblemViewTest(TestCase):
    fixtures = ["testdatabase.yaml"]

    def setUp(self):
        self.base_url = "/api/problem/"
        self.factory = APIRequestFactory()
        self.view = ProblemView.as_view()

    def testZ_get_problem(self):
        ac_data = {
            "title": "Simple Problem",
            "description": "This is description",
            "pid": 5,
            "allow_html": False,
            "enabled": True,
            "tags": [1, 2, 3],
        }

        request = self.factory.get(self.base_url)
        response = self.view(request, pid=5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("res")
        self.assertIsNotNone(data)

        self.assertEqual(data.get("title"), ac_data["title"])
        self.assertEqual(data.get("description"), ac_data["description"])
        self.assertEqual(data.get("pid"), ac_data["pid"])
        self.assertEqual(data.get("allow_html"), ac_data["allow_html"])
        self.assertEqual(data.get("enabled"), ac_data["enabled"])
        self.assertEqual(data.get("tags"), ac_data["tags"])
