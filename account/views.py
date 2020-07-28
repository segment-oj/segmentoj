from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from segmentoj import tools
from segmentoj.decorator import syllable_required, parameter_required
from account.models import User
from account.serializers import AccountSerializer

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
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
        except IntegrityError:
            # failed, probably because username already exits
            return Response(
                {"detail": "Failed to create user."}, status=status.HTTP_409_CONFLICT
            )

        if user:  # Success
            user.save()  # Save user

            return Response(
                {"detail": "Success", "res": {"id": user.id}},
                status=status.HTTP_201_CREATED,
            )
        else:  # failed, probably because username already exits
            return Response(
                {"detail": "Failed to create user."}, status=status.HTTP_409_CONFLICT
            )


class AccountUsernameAccessibilityView(APIView):
    @method_decorator(parameter_required("username"))
    def get(self, request, username):
        account_filter = {"username": username}

        queryset = User.objects.filter(**account_filter)
        if queryset.count() == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_409_CONFLICT)
