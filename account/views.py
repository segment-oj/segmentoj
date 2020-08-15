from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.conf import settings

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.utils import timezone

from datetime import timedelta
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from segmentoj import tools
from segmentoj.decorator import syllable_required, parameter_required, login_required
from captcha.decorator import captcha_required
from .models import User
from .serializers import AccountSerializer, AccountIntroductionSerializer
from .decorator import password_verify_required

import os.path
import base64

# Create your views here.
class AccountSessionView(APIView):

    # Create user session(Login)
    @method_decorator(syllable_required("username", str))
    @method_decorator(syllable_required("password", str))
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return Response(
                {"detail": "Success", "res": {"id": user.id}},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Username or password wrong"},
                status=status.HTTP_403_FORBIDDEN,
            )

    # delete session(logout)
    def delete(self, request):

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Not logged in!"}, status=status.HTTP_401_UNAUTHORIZED
            )

        auth.logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AccountIntroductionView(APIView):

    # Get User Introduction
    @method_decorator(parameter_required("uid"))
    def get(self, request, uid):
        user = get_object_or_404(User, id=uid)
        us = AccountIntroductionSerializer(user)
        return Response({"res": us.data}, status=status.HTTP_200_OK)

    @method_decorator(parameter_required("uid"))
    def patch(self, request, uid):
        if not request.user.has_perm("account.change_user"):
            if request.user.id != uid:
                return Response({
                    "detail": "You have no permission to change this user"
                }, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        user = get_object_or_404(User, id=uid)
        us = AccountIntroductionSerializer(user, data=data, partial=True)
        us.is_valid(raise_exception=True)
        us.save()

        return Response({
            "detail": "Success"
        }, status=status.HTTP_204_NO_CONTENT)

class AccountView(APIView):

    # Get User Infomation Except Introduction
    @method_decorator(parameter_required("uid"))
    def get(self, request, uid):
        user = get_object_or_404(User, id=uid)
        us = AccountSerializer(user)
        return Response({"res": us.data}, status=status.HTTP_200_OK)

    # Create New User(register an account)
    @method_decorator(syllable_required("username", str))
    @method_decorator(syllable_required("password", str))
    @method_decorator(syllable_required("email", str))
    @method_decorator(captcha_required())
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if len(password) < 6:
            return Response(
                {"detail": "Password too short"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not tools.isEmail(email):
            return Response(
                {"detail": "Email is not correct"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            # failed, probably because username already exits
            return Response({"detail": "Failed to create user."}, status=status.HTTP_409_CONFLICT)

        if user:  # Success
            user.save()  # Save user

            return Response(
                {"detail": "Success", "res": {"id": user.id}},
                status=status.HTTP_201_CREATED,
            )
        else:  # failed, probably because username already exits
            return Response({"detail": "Failed to create user."}, status=status.HTTP_409_CONFLICT)

    @method_decorator(parameter_required("uid"))
    def patch(self, request, uid):
        data = request.data
        user = get_object_or_404(User, id=uid)

        if not request.user.has_perm("account.change_user"):
            if request.user.id != user.id:
                return Response({
                    "detail": "You have no permission to change this user"
                }, status=status.HTTP_403_FORBIDDEN)

            request_is_active = data.get("is_active")
            request_is_staff = data.get("is_staff")
            request_is_superuser = data.get("is_superuser")

            if request_is_active != None and request_is_active != user.is_active:
                return Response({
                    "detail": "You have no permission to change this user"
                }, status=status.HTTP_403_FORBIDDEN)

            if request_is_staff != None and request_is_staff != user.is_staff:
                return Response({
                    "detail": "You have no permission to change this user"
                }, status=status.HTTP_403_FORBIDDEN)

            if request_is_superuser != None and request_is_superuser != user.is_superuser:
                return Response({
                    "detail": "You have no permission to change this user"
                }, status=status.HTTP_403_FORBIDDEN)

        us = AccountSerializer(user, data=data, partial=True)
        us.is_valid(raise_exception=True)
        us.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AccountPasswordView(APIView):
    @method_decorator(login_required())
    @method_decorator(syllable_required("password", str))
    def post(self, request):
        # Verify
        data = request.data
        user = request.user
        pwd = data.get("password")
        if user.check_password(pwd):
            request.session["password_verified"] = True
            return Response({
                "detail": "Verify Password OK."
            }, status=status.HTTP_201_CREATED)

        return Response({
            "detail": "Password incorrect!"
        }, status=status.HTTP_403_FORBIDDEN)

    @method_decorator(login_required())
    @method_decorator(syllable_required("password", str))
    @method_decorator(password_verify_required())
    def patch(self, request):
        data = request.data
        user = request.user
        pwd = data.get("password")
        user.set_password(pwd)
        user.save()

        return Response({
            "detail": "Success"
        }, status=status.HTTP_204_NO_CONTENT)

class AccountUsernameAccessibilityView(APIView):
    @method_decorator(parameter_required("username"))
    def get(self, request, username):
        account_filter = {"username": username}

        queryset = User.objects.filter(**account_filter)
        if queryset.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_409_CONFLICT)

class AccountAvatarView(APIView):

    def get(self, request, uid):
        avatar_path = os.path.join(settings.MEDIA_ROOT, "avatar", "{uid}.png".format(uid=uid))

        if not os.path.isfile(avatar_path):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        avatar_uri = os.path.join(settings.MEDIA_URL, "avatar", "{uid}.png".format(uid=uid))
        return Response({
            "res": avatar_uri
        }, status=status.HTTP_200_OK)

    @method_decorator(login_required())
    @method_decorator(captcha_required())
    def put(self, request):
        uid = request.user.id
        avatar_file = request.FILES.get("avatar")

        if not avatar_file:
            return Response({
                "detail": "avatar img file missing"
            }, status=status.HTTP_400_BAD_REQUEST)

        if avatar_file.size > 5120: # 5M
            return Response({
                "detail": "avatar img too large"
            })
        
        filepath = os.path.join(settings.MEDIA_ROOT, "avatar", "{uid}.png".format(uid=uid))
        try:
            with open(filepath, "wb+") as f:
                for chunk in avatar_file.chunks(): 
                    f.write(chunk)
        except Exception as e:
            return Response({
                "detail": "Failed to save img"
            }, status=status.HTTP_201_CREATED)

    @method_decorator(parameter_required("uid"))
    @method_decorator(permission_required("account.edit_user", raise_exception=True))
    def delete(self, request, uid):
        avatar_path = os.path.join(settings.MEDIA_ROOT, "avatar", "{uid}.png".format(uid=uid))

        if not os.path.isfile(avatar_path):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        os.remove(avatar_path)
        return Response(status=status.HTTP_200_OK)

class AccountEmailView(APIView):

    @method_decorator(login_required())
    def get(self, request):
        return Response({
            "res": request.user.email
        })

    @method_decorator(login_required())
    def post(self, request, vid=None):
        signer = TimestampSigner()
        user = request.user
        if vid == None:
            # send mail
            signature = signer.sign(user.username)
            signature = base64.urlsafe_b64encode(signature.encode())
            signature = signature.decode()
            user.email_user(settings.VERIFY_EMAIL_TEMPLATE_TITLE, 
                            settings.VERIFY_EMAIL_TEMPLATE_CONTENT.format(username=user.username, signature=signature),
                            html_message=settings.VERIFY_EMAIL_TEMPLATE_CONTENT.format(username=user.username, signature=signature),)
            return Response({
                "detail": "Email sent"
            }, status=status.HTTP_202_ACCEPTED)

        vid = base64.urlsafe_b64decode(vid.encode())
        vid = vid.decode()
        try:
            value = signer.unsign(vid, max_age=timedelta(minutes=settings.VERIFY_EMAIL_MAX_AGE))
        except SignatureExpired:
            return Response({
                "detail": "Signature Expired"
            }, status=status.HTTP_403_FORBIDDEN)
        except BadSignature:
            return Response({
                "detail": "Bad Signature"
            }, status=status.HTTP_403_FORBIDDEN)
        
        if value != user.username:
            return Response({
                "detail": "Mismatch Signature"
            }, status=status.HTTP_403_FORBIDDEN)
        
        user.email_verified = True
        user.save()
        request.session["email_verified"] = True
        return Response({
            "detail": "Susccess"
        }, status=status.HTTP_204_NO_CONTENT)

    @method_decorator(syllable_required("email", str))
    @method_decorator(password_verify_required())
    def patch(self, request):
        # change email

        data = request.data
        user = request.user
        
        user.email = data.get("email")
        user.email_verified = False
        user.save()

        return Response({
            "detail": "Success"
        }, status.HTTP_204_NO_CONTENT)