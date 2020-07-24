from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import StatusView
from account.models import User

import status.JudgeLanguage as jl
import status.JudgeStatus as js

# Create your tests here.
class StatusTest(TestCase):
    fixtures = ["testdatabase.yaml"]

    # setup test case
    def setUp(self):
        self.base_url = "/api/status"
        self.view = StatusView.as_view()
        self.factory = APIRequestFactory()

    def testA_submit_problem(self):
        request_data = {
            "problem": 1,
            "code": "# This is the code.",
        }

        user = User.objects.get(username="testuser")

        request = self.factory.post(self.base_url, request_data, format="json")
        force_authenticate(request, user)
        res = self.view(request)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def testB_get_status(self):
        ac_data = {
            "id": 1,
            "score": 100,
            "state": js.JUDGE_STATUS_AC,
            "lang": jl.JUDGE_LANGUAGE_CPP,
            "code": "# Code",
            "problem": 1,
            "owner": 2,
        }

        request = self.factory.get(self.base_url, format="json")
        res = self.view(request, sid=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        data = res.data["res"]

        self.assertEqual(data.get("id"), ac_data["id"])
        self.assertEqual(data.get("score"), ac_data["score"])
        self.assertEqual(data.get("state"), ac_data["state"])
        self.assertEqual(data.get("lang"), ac_data["lang"])
        self.assertEqual(data.get("code"), ac_data["code"])
        self.assertEqual(data.get("problem"), ac_data["problem"])
        self.assertEqual(data.get("owner"), ac_data["owner"])

    # Try to submit problem without logged in
    def testC_submit_problem_not_login(self):
        request_data = {
            "problem": 1,
            "code": "# This is the code.",
        }

        user = User.objects.get(username="testuser")

        request = self.factory.post(self.base_url, request_data, format="json")
        force_authenticate(request)  # Clear Session
        res = self.view(request)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
