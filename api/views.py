from django.contrib.auth.models import User
from django.contrib import auth

from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import json

# Create your views here.

class UserView(APIView):

	@method_decorator(csrf_exempt)
	def post(self, request):
		# Create user session(Login)
		data = request.data
		username = data['username']
		password = data['password']

		user = auth.authenticate(request,username=username,password=password)

		if user:
			auth.login(request, user)
			return Response({"msg": "done."}, status=status.HTTP_201_CREATED)
		else:
			return Response({"msg": "Username or password wrong"}, status=status.HTTP_403_FORBIDDEN)

	@method_decorator(csrf_exempt)
	def delete(self, request):
		# delete session(logout)

		if not request.user.is_authenticated:
			return Response({"msg": "Not logged in!"}, status=status.HTTP_401_UNAUTHORIZED)
		
		auth.logout(request)
		return Response({"msg": "Success!"}, status=status.HTTP_205_RESET_CONTENT)
	

