from django.contrib.auth.models import User
from django.contrib import auth

from django.db.utils import IntegrityError

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import json

from segmentoj import tools

# Create your views here.

class UserView(APIView):

	def post(self, request):
		# Create user session(Login)
		data = request.data
		username = data.get('username')
		password = data.get('password')

		if not username or not password:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		user = auth.authenticate(request,username=username,password=password)

		if user:
			auth.login(request, user)
			return Response({
				"msg": "Success",
				"res": {
					"id": user.id
				}}, status=status.HTTP_201_CREATED)
		else:
			return Response({"msg": "Username or password wrong"}, status=status.HTTP_403_FORBIDDEN)

	def delete(self, request):
		# delete session(logout)

		if not request.user.is_authenticated:
			return Response({"msg": "Not logged in!"}, status=status.HTTP_401_UNAUTHORIZED)
		
		auth.logout(request)
		return Response(status=status.HTTP_204_NO_CONTENT)
	
	def put(self, request):
		# put a record(register an account)

		username = request.data.get('username')
		password = request.data.get('password')
		email = request.data.get('email')

		if not username or not password or not email:
			return Response(status.HTTP_400_BAD_REQUEST)

		if not tools.isEmail(email):
			return Response({"msg": "Email is not correct!"}, status=status.HTTP_400_BAD_REQUEST)

		try: 
			user = auth.models.User.objects.create_user(username=username, password=password, email=email)
		except IntegrityError:
			# failed, probably because username already exits
			return Response({"msg": "Failed to create user."}, status=status.HTTP_409_CONFLICT)

		if user: # Success
			user.save() # Save user

			return Response(status=status.HTTP_201_CREATED)
		else: # failed, probably because username already exits
			return Response({"msg": "Failed to create user."}, status=status.HTTP_409_CONFLICT)


		

