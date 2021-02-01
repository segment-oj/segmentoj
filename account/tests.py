from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate

from .views import (
    AccountView,
    AccountIntroductionView,
    AccountUsernameAccessibilityView,
    AccountPasswordView,
)
from .models import Account
from captcha.models import CaptchaStore

# Create your tests here.
class AccountViewTest(TestCase):
    fixtures = ["testdatabase.yaml"]

    # setup test case
    def setUp(self):
        self.base_url = "/api/account"
        self.factory = APIRequestFactory()
        self.view = AccountView.as_view()

    # test adding a user
    def testA_add_user(self):
        request_data = {
            "username": "unittesuser01",
            "email": "unittesuser01@soj.ac.cn",
            "password": "unittest",
            "captcha_key": 1234,
            "captcha_answer": "unit"
        }

        c = CaptchaStore(key=request_data["captcha_key"], answer=request_data["captcha_answer"])
        c.save()

        request = self.factory.post(self.base_url, data=request_data, format="json")
        res = self.view(request)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_json = res.data
        self.assertEqual(type(res_json["res"]["id"]), int)

    def testB_get_user(self):
        user_data = {
            "id": 1,
            "username": "admin",
            "email": "admin@soj.ac.cn",
            "lang": 0,
            "is_staff": True,
            "is_active": True,
            "is_superuser": True,
            "list_column": 20,
            "editor_theme": 0,
            "nav_color": "#000000"
        }

        request = self.factory.get(self.base_url)
        res = self.view(request, uid=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res_json = res.data
        res_data = res_json["res"]

        self.assertEqual(res_data.get("id"), user_data["id"])
        self.assertEqual(res_data.get("username"), user_data["username"])
        self.assertEqual(res_data.get("lang"), user_data["lang"])
        self.assertEqual(res_data.get("is_staff"), user_data["is_staff"])
        self.assertEqual(res_data.get("is_active"), user_data["is_active"])
        self.assertEqual(res_data.get("is_superuser"), user_data["is_superuser"])
        self.assertEqual(res_data.get("list_column"), user_data["list_column"])
        self.assertEqual(res_data.get("editor_theme"), user_data["editor_theme"])
        self.assertEqual(res_data.get("nav_color"), user_data["nav_color"])

    def testC_get_404_user(self):
        request = self.factory.get(self.base_url)
        res = self.view(request, uid=-1)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def testE_add_exit_user(self):
        request_data = {
            "username": "unittesuser02",
            "email": "unittesuser02@soj.ac.cn",
            "password": "unittest",
            "captcha_key": 4456,
            "captcha_answer": "ut2x"
        }

        c = CaptchaStore(key=request_data["captcha_key"], answer=request_data["captcha_answer"])
        c.save()

        request = self.factory.post(self.base_url, data=request_data, format="json")
        self.view(request)

        c = CaptchaStore(key=request_data["captcha_key"], answer=request_data["captcha_answer"])
        c.save()

        request = self.factory.post(self.base_url, data=request_data, format="json")
        res = self.view(request)
        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def testF_add_user_miss_sth(self):
        request_data = {
            "username": "unittesuser03",
            "email": "unittesuser03@soj.ac.cn",
        }

        request = self.factory.post(self.base_url, data=request_data, format="json")
        res = self.view(request)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def testG_get_user_miss_uid(self):
        request = self.factory.get(self.base_url, format="json")
        res = self.view(request)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def testH_change_user_admin(self):
        request_data = {
            "username": "testusernewname",
            "is_superuser": True,
            "is_staff": True
        }

        request = self.factory.patch(self.base_url, data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="admin"))
        res = self.view(request, uid=2)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(id=2)
        self.assertEqual(target.username, request_data["username"])
        self.assertEqual(target.is_superuser, request_data["is_superuser"])
        self.assertEqual(target.is_staff, request_data["is_staff"])

    def testI_change_user_own(self):
        request_data = {
            "username": "zhangtianlinewname",
            "lang": 5,
            "list_column": 100,
            "editor_theme": 2
        }

        request = self.factory.patch(self.base_url, data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="zhangtianli"))
        res = self.view(request, uid=3)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(id=3)
        self.assertEqual(target.username, request_data["username"])
        self.assertEqual(target.lang, request_data["lang"])
        self.assertEqual(target.list_column, request_data["list_column"])
        self.assertEqual(target.editor_theme, request_data["editor_theme"])
    
    def testJ_change_user_admin(self):
        request_data = {
            "is_active": False
        }

        request = self.factory.patch(self.base_url, data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="admin"))
        res = self.view(request, uid=2)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(id=2)
        self.assertEqual(target.is_active, request_data["is_active"])

    def testK_change_user_not_admin(self):
        request_data = {
            "is_active": False
        }

        request = self.factory.patch(self.base_url, data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="testuser"))
        res = self.view(request, uid=3)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def testL0_change_not_admin(self):
        request_data = {
            "is_active": False
        }

        ac_data = {
            "is_active": True
        }

        request = self.factory.patch(self.base_url, data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="testuser"))
        res = self.view(request, uid=2)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        target = Account.objects.get(id=2)
        self.assertEqual(target.is_active, ac_data["is_active"])

class AccountIntroductionViewTest(TestCase):
    fixtures = ["testdatabase.yaml"]

    def setUp(self):
        self.base_url = "/api/account/{uid}/introduction"
        self.factory = APIRequestFactory()
        self.view = AccountIntroductionView.as_view()

    def testZ_get_user_introduction(self):
        ac_data = {
            "introduction": "# Hello World!",
        }

        request = self.factory.get(self.base_url.format(uid=1))
        response = self.view(request, uid=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get("res")
        self.assertIsNotNone(data)

        self.assertEqual(data.get("introduction"), ac_data["introduction"])

    def testY_admin_patch_own_introduction(self):
        request_data = {
            "introduction": "Modified!",
        }

        request = self.factory.patch(self.base_url.format(uid=1), data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="admin"))
        response = self.view(request, uid=1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testX_admin_patch_other_introduction(self):
        request_data = {
            "introduction": "Modified!",
        }

        request = self.factory.patch(self.base_url.format(uid=2), data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="admin"))
        response = self.view(request, uid=2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testW_user_patch_own_introduction(self):
        request_data = {
            "introduction": "Modified!",
        }

        request = self.factory.patch(self.base_url.format(uid=2), data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="testuser"))
        response = self.view(request, uid=2)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testV_user_patch_other_introduction_failed(self):
        request_data = {
            "introduction": "Modified!",
        }

        request = self.factory.patch(self.base_url.format(uid=1), data=request_data, format="json")
        force_authenticate(request, Account.objects.get(username="testuser"))
        response = self.view(request, uid=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AccountPasswordViewTest(TestCase):
    fixtures = ["testdatabase.yaml"]

    def setUp(self):
        self.base_url = "/api/account/password"
        self.client = APIClient()
        self.client.force_authenticate(user=Account.objects.get(username="admin"))

    def testZ_verify_password_ok(self):
        request_data = {
            "password": "123456"
        }

        response = self.client.post(self.base_url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testY_verify_password_wrong(self):
        request_data = {
            "password": "wrong password"
        }

        response = self.client.post(self.base_url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def testX_change_password(self):
        request_data = {
            "password": "123456"
        }

        self.client.post(self.base_url, request_data, format='json')

        request_data = {
            "password": "new password"
        }

        response = self.client.patch(self.base_url, request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(username="admin")
        self.assertTrue(target.check_password(request_data["password"]))

class AccountUsernameAccessibilityViewTest(TestCase):
    fixtures = ["testdatabase.yaml"]

    def setUp(self):
        self.base_url = "/api/account/username/accessibility/"
        self.factory = APIRequestFactory()
        self.view = AccountUsernameAccessibilityView.as_view()

    def testZ_get_accessibility_fail(self):
        request = self.factory.get(self.base_url)
        response = self.view(request, username="unittest")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testY_get_accessibility_ok(self):
        request = self.factory.get(self.base_url)
        response = self.view(request, username="admin")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
