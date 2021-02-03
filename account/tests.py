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
    fixtures = ['testdatabase.yaml']

    # setup test case
    def setUp(self):
        self.base_url = '/api/account'
        self.factory = APIRequestFactory()
        self.view = AccountView.as_view()

    # test adding a user
    def testA_add_user(self):
        request_data = {
            'username': 'unittesuser01',
            'email': 'unittesuser01@soj.ac.cn',
            'password': 'unittest',
            'captcha_key': 1234,
            'captcha_answer': 'unit'
        }

        c = CaptchaStore(key=request_data['captcha_key'], answer=request_data['captcha_answer'])
        c.save()

        request = self.factory.post(self.base_url, data=request_data, format='json')
        res = self.view(request)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_json = res.data
        self.assertEqual(type(res_json['res']['id']), int)

    def testB_get_user(self):
        user_data = {
            'id': 1,
            'username': 'admin',
            'email': 'admin@soj.ac.cn',
            'lang': 'cxx;17,clang,O2',
            'is_staff': True,
            'is_active': True,
            'is_superuser': True,
        }

        request = self.factory.get(self.base_url)
        res = self.view(request, uid=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res_json = res.data
        res_data = res_json['res']

        self.assertEqual(res_data.get('id'), user_data['id'])
        self.assertEqual(res_data.get('username'), user_data['username'])
        self.assertEqual(res_data.get('lang'), user_data['lang'])
        self.assertEqual(res_data.get('is_staff'), user_data['is_staff'])
        self.assertEqual(res_data.get('is_active'), user_data['is_active'])
        self.assertEqual(res_data.get('is_superuser'), user_data['is_superuser'])

    def testC_get_404_user(self):
        request = self.factory.get(self.base_url)
        res = self.view(request, uid=-1)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def testE_add_exit_user(self):
        request_data = {
            'username': 'unittesuser02',
            'email': 'unittesuser02@soj.ac.cn',
            'password': 'unittest',
            'captcha_key': 4456,
            'captcha_answer': 'ut2x'
        }

        c = CaptchaStore(key=request_data['captcha_key'], answer=request_data['captcha_answer'])
        c.save()

        request = self.factory.post(self.base_url, data=request_data, format='json')
        self.view(request)

        c = CaptchaStore(key=request_data['captcha_key'], answer=request_data['captcha_answer'])
        c.save()

        request = self.factory.post(self.base_url, data=request_data, format='json')
        res = self.view(request)
        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def testF_add_user_miss_sth(self):
        request_data = {
            'username': 'unittesuser03',
            'email': 'unittesuser03@soj.ac.cn',
        }

        request = self.factory.post(self.base_url, data=request_data, format='json')
        res = self.view(request)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def testG_get_user_miss_uid(self):
        request = self.factory.get(self.base_url, format='json')
        res = self.view(request)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
    
    def testH_change_user_admin(self):
        request_data = {
            'username': 'testusernewname',
            'is_superuser': True,
            'is_staff': True
        }

        request = self.factory.patch(self.base_url, data=request_data, format='json')
        force_authenticate(request, Account.objects.get(username='admin'))
        res = self.view(request, uid=2)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(id=2)
        self.assertEqual(target.username, request_data['username'])
        self.assertEqual(target.is_superuser, request_data['is_superuser'])
        self.assertEqual(target.is_staff, request_data['is_staff'])

    def testI_change_user_own(self):
        request_data = {
            'username': 'szdytom_newname',
            'lang': 'js',
        }

        target = Account.objects.get(username='szdytom')
        request = self.factory.patch(self.base_url, data=request_data, format='json')
        force_authenticate(request, target)
        res = self.view(request, uid=target.id)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(id=target.id)
        self.assertEqual(target.username, request_data['username'])
        self.assertEqual(target.lang, request_data['lang'])
    
    def testJ_change_user_admin(self):
        request_data = {
            'is_active': False
        }

        target = Account.objects.get(username='admin')
        request = self.factory.patch(self.base_url, data=request_data, format='json')
        force_authenticate(request, target)
        res = self.view(request, uid=target.id)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(username='admin')
        self.assertEqual(target.is_active, request_data['is_active'])

    def testK_change_user_not_admin(self):
        request_data = {
            'is_active': False
        }

        target = Account.objects.get(username='szdytom')
        request = self.factory.patch(self.base_url, data=request_data, format='json')
        force_authenticate(request, target)
        res = self.view(request, uid=target.id)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def testL0_change_not_admin(self):
        request_data = {
            'is_active': False
        }

        ac_data = {
            'is_active': True
        }

        request = self.factory.patch(self.base_url, data=request_data, format='json')
        force_authenticate(request, Account.objects.get(username='szdytom'))
        res = self.view(request, uid=1)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        target = Account.objects.get(id=1)
        self.assertEqual(target.is_active, ac_data['is_active'])

class AccountIntroductionViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/account/{uid}/introduction'
        self.factory = APIRequestFactory()
        self.view = AccountIntroductionView.as_view()

    def testZ_get_user_introduction(self):
        target = Account.objects.get(username='szdytom')
        ac_data = {
            'introduction': target.introduction,
        }

        request = self.factory.get(self.base_url.format(uid=target.id))
        response = self.view(request, uid=target.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data.get('res')
        self.assertIsNotNone(data)

        self.assertEqual(data.get('introduction'), ac_data['introduction'])

    def testY_admin_patch_own_introduction(self):
        request_data = {
            'introduction': 'Modified!',
        }

        target = Account.objects.get(username='admin')
        request = self.factory.patch(self.base_url.format(uid=target.id), data=request_data, format='json')
        force_authenticate(request, target)
        response = self.view(request, uid=target.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testX_admin_patch_other_introduction(self):
        request_data = {
            'introduction': 'Modified!',
        }

        target = Account.objects.get(username='szdytom')
        request = self.factory.patch(self.base_url.format(uid=target.id), data=request_data, format='json')
        force_authenticate(request, Account.objects.get(username='admin'))
        response = self.view(request, uid=target.id)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(username='szdytom')
        self.assertEqual(target.introduction, request_data['introduction'])

    def testW_user_patch_own_introduction(self):
        request_data = {
            'introduction': 'Modified!',
        }

        target = Account.objects.get(username='fat')
        request = self.factory.patch(self.base_url.format(uid=target.id), data=request_data, format='json')
        force_authenticate(request, target)
        response = self.view(request, uid=target.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        target = Account.objects.get(username='fat')
        self.assertEqual(target.introduction, request_data['introduction'])

    def testV_user_patch_other_introduction_failed(self):
        request_data = {
            'introduction': 'Modified!',
        }

        request = self.factory.patch(self.base_url.format(uid=1), data=request_data, format='json')
        force_authenticate(request, Account.objects.get(username='fat'))
        response = self.view(request, uid=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AccountPasswordViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/account/password'
        self.factory = APIRequestFactory()
        self.view = AccountPasswordView.as_view()

    def testZ_change_user_password(self):
        req_data = {
            'current_password': '123456',
            'password': '654321',
        }

        user = Account.objects.get(username='admin')
        request = self.factory.patch(self.base_url, req_data)
        force_authenticate(request, user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(user.check_password('654321'))

class AccountUsernameAccessibilityViewTest(TestCase):
    fixtures = ['testdatabase.yaml']

    def setUp(self):
        self.base_url = '/api/account/username/accessibility/'
        self.factory = APIRequestFactory()
        self.view = AccountUsernameAccessibilityView.as_view()

    def testZ_get_accessibility_unused(self):
        request = self.factory.get(self.base_url)
        response = self.view(request, username='unittest')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def testY_get_accessibility_used(self):
        request = self.factory.get(self.base_url)
        response = self.view(request, username='admin')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
