from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import JudgerStatusView, JudgerStatusDetailView
from account.models import User
from status import JudgeLanguage as jl
from status import JudgeStatus as js

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

class JudgerStatusDetailTest(TestCase):
    fixtures = ["testdatabase.yaml"]

    def setUp(self):
        self.base_url = "/api/judger/status"
        self.factory = APIRequestFactory()
        self.view = JudgerStatusDetailView.as_view()

    def testA_get_submit_detail(self):
        ac_data = {
            "code": "#include <cstdio>\r\nusing namespace std;\r\n\r\nint main() {\r\n    int a, b;\r\n    scanf(\"%d %d\", &a, &b);\r\n    printf(\"%d\\n\", a + b);\r\n    return 0;\r\n}",
            "problem": 1,
            "lang": jl.JUDGE_LANGUAGE_CPP,
            "id": 3
        }

        request = self.factory.get(self.base_url)
        force_authenticate(request, user=User.objects.get(username="ForcesEqual"))
        response = self.view(request, sid=3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data.get("res")
        self.assertIsNotNone(data)
        self.assertEqual(data.get("code"), ac_data["code"])
        self.assertEqual(data.get("problem"), ac_data["problem"])
        self.assertEqual(data.get("lang"), ac_data["lang"])
        self.assertEqual(data.get("id"), ac_data["id"])
    
    def testB_post_detail(self):
        request_data = {
            "state": js.JUDGE_STATUS_AC,
            "time": 200,
            "memory": 8500,
            "score": 100,
            "input_s": "1 2",
            "output_s": "3",
            "error_s": "",
            "answer_s": "3"
        }

        request = self.factory.post(self.base_url, data=request_data, format="json")
        force_authenticate(request, user=User.objects.get(username="ForcesEqual"))
        response = self.view(request, sid=3, cid=1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def testC_post_detail_partly(self):
        request_data = {
            "state": js.JUDGE_STATUS_AC,
            "time": 203,
            "memory": 8501,
            "score": 100
        }

        request = self.factory.post(self.base_url, data=request_data, format="json")
        force_authenticate(request, user=User.objects.get(username="ForcesEqual"))
        response = self.view(request, sid=3, cid=2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testD_post_detail_same_twice(self):
        request_data = {
            "state": js.JUDGE_STATUS_JUDGING,
        }

        request = self.factory.post(self.base_url, data=request_data, format="json")
        force_authenticate(request, user=User.objects.get(username="ForcesEqual"))
        response = self.view(request, sid=3, cid=3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request_data = {
            "state": js.JUDGE_STATUS_AC,
            "time": 200,
            "memory": 8500,
            "score": 100,
            "input_s": "10 20",
            "output_s": "30",
            "error_s": "",
            "answer_s": "30",
        }

        request = self.factory.post(self.base_url, data=request_data, format="json")
        force_authenticate(request, user=User.objects.get(username="ForcesEqual"))
        response = self.view(request, sid=3, cid=3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)