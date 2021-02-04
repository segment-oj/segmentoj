from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.conf import settings

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.core.signing import TimestampSigner

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from segmentoj import tools
from segmentoj.decorator import syllable_required, parameter_required, login_required
from captcha.decorator import captcha_required
from .models import Account
from .serializers import AccountSerializer, AccountIntroductionSerializer
from .decorator import email_verification_required, password_verification_required

import os.path
import base64

# Create your views here.
class AccountSessionView(APIView):

    # Create user session(Login)
    @method_decorator(syllable_required('username', str))
    @method_decorator(syllable_required('password', str))
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return Response(
                {'detail': 'Success', 'res': {'id': user.id}},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {'detail': 'Username or password wrong'},
                status=status.HTTP_403_FORBIDDEN,
            )

    # delete session(logout)
    def delete(self, request):

        if not request.user.is_authenticated:
            return Response({'detail': 'Not logged in!'}, status=status.HTTP_401_UNAUTHORIZED)

        auth.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountIntroductionView(APIView):

    # Get User Introduction
    @method_decorator(parameter_required('uid'))
    def get(self, request, uid):
        user = get_object_or_404(Account, id=uid)
        us = AccountIntroductionSerializer(user)
        return Response({'res': us.data}, status=status.HTTP_200_OK)

    @method_decorator(parameter_required('uid'))
    def patch(self, request, uid):
        if not request.user.has_perm('account.change_user'):
            if request.user.id != uid:
                return Response(
                    {'detail': 'You have no permission to change this user'}, status=status.HTTP_403_FORBIDDEN
                )

        data = request.data
        user = get_object_or_404(Account, id=uid)
        us = AccountIntroductionSerializer(user, data=data, partial=True)
        us.is_valid(raise_exception=True)
        us.save()

        return Response({'detail': 'Success'}, status=status.HTTP_204_NO_CONTENT)


class AccountView(APIView):

    # Get User Infomation Except Introduction
    @method_decorator(parameter_required('uid'))
    def get(self, request, uid):
        user = get_object_or_404(Account, id=uid)
        us = AccountSerializer(user)
        return Response({'res': us.data}, status=status.HTTP_200_OK)

    # Create New User(register an account)
    @method_decorator(syllable_required('username', str))
    @method_decorator(syllable_required('password', str))
    @method_decorator(syllable_required('email', str))
    @method_decorator(captcha_required())
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if len(password) < 6:
            return Response({'detail': 'Password too short'}, status=status.HTTP_400_BAD_REQUEST)

        if not tools.isEmail(email):
            return Response({'detail': 'Email is not correct'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Account.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            # failed, probably because username already exits
            return Response({'detail': 'Failed to create user.'}, status=status.HTTP_409_CONFLICT)

        if user:  # Success
            user.save()  # Save user

            return Response(
                {'detail': 'Success', 'res': {'id': user.id}},
                status=status.HTTP_201_CREATED,
            )
        else:  # failed, probably because username already exits
            return Response({'detail': 'Failed to create user.'}, status=status.HTTP_409_CONFLICT)

    @method_decorator(parameter_required('uid'))
    def patch(self, request, uid):
        data = request.data
        user = get_object_or_404(Account, id=uid)

        if not request.user.has_perm('account.change_user'):
            if request.user.id != user.id:
                return Response(
                    {'detail': 'You have no permission to change this user'}, status=status.HTTP_403_FORBIDDEN
                )

            request_is_active = data.get('is_active')
            request_is_staff = data.get('is_staff')
            request_is_superuser = data.get('is_superuser')

            if request_is_active != None and request_is_active != user.is_active:
                return Response(
                    {'detail': 'You have no permission to change this user'}, status=status.HTTP_403_FORBIDDEN
                )

            if request_is_staff != None and request_is_staff != user.is_staff:
                return Response(
                    {'detail': 'You have no permission to change this user'}, status=status.HTTP_403_FORBIDDEN
                )

            if request_is_superuser != None and request_is_superuser != user.is_superuser:
                return Response(
                    {'detail': 'You have no permission to change this user'}, status=status.HTTP_403_FORBIDDEN
                )

        us = AccountSerializer(user, data=data, partial=True)
        us.is_valid(raise_exception=True)
        us.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountPasswordView(APIView):
    @method_decorator(login_required())
    @method_decorator(syllable_required('password', str))
    @method_decorator(password_verification_required())
    def patch(self, request):
        data = request.data
        user = request.user
        pwd = data.get('password')
        user.set_password(pwd)
        user.save()

        return Response({'detail': 'Success'}, status=status.HTTP_204_NO_CONTENT)


class AccountUsernameAccessibilityView(APIView):
    @method_decorator(parameter_required('username'))
    def get(self, request, username):
        account_filter = {'username': username}

        queryset = Account.objects.filter(**account_filter)
        if queryset.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_409_CONFLICT)

class AccountEmailView(APIView):
    @method_decorator(login_required())
    def get(self, request):
        return Response({'res': request.user.email})

    @method_decorator(login_required())
    @method_decorator(captcha_required())
    def post(self, request, vid=None):
        signer = TimestampSigner()
        user = request.user
        signature = signer.sign(user.username)
        signature = base64.urlsafe_b64encode(signature.encode())
        signature = signature.decode()
        user.email_user(
            settings.VERIFY_EMAIL_TEMPLATE_TITLE,
            settings.VERIFY_EMAIL_TEMPLATE_CONTENT.format(username=user.username, signature=signature),
            html_message=settings.VERIFY_EMAIL_TEMPLATE_CONTENT.format(username=user.username, signature=signature),
        )
        return Response({'detail': 'Email sent'}, status=status.HTTP_202_ACCEPTED)

    @method_decorator(syllable_required('email', str))
    @method_decorator(email_verification_required())
    @method_decorator(password_verification_required())
    def patch(self, request):
        # change email

        data = request.data
        user = request.user

        user.email = data.get('email')
        user.email_verified = False
        user.save()

        return Response({'detail': 'Success'}, status.HTTP_204_NO_CONTENT)
