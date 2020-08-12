from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.conf import settings

from django.utils.decorators import method_decorator, permission_required
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from segmentoj import tools
from segmentoj.decorator import syllable_required, parameter_required, login_required
from captcha.decorator import captcha_required
from account.models import User
from account.serializers import AccountSerializer

import os.path

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


class AccountView(APIView):

    # Get User Infomation
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
            
            data.pop("is_active", None)
            data.pop("is_staff", None)
            data.pop("is_superuser", None)

        us = AccountSerializer(user, data=data, partial=True)
        us.is_valid(raise_exception=True)
        us.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
