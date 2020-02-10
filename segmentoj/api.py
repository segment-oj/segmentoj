# api request response code
from django.contrib import auth
from django.http import JsonResponse
import json

def login_api(request):
	data = json.loads(request.body)

	username = data['username']
	password = data['password']

	user = auth.authenticate(request,username=username,password=password)

	if user:
		# authenticate success
		auth.login(request,user);
		data = {
			'code': 0,
			'msg': "Hello, {name}".format(name=username)
		}

		return JsonResponse(data)
	else:
		# failed
		data = {
			'code': 1,
			'msg': 'Username or password wrong, authenticate failed.'
		}

		return JsonResponse(data)

def logout_api(request):
	auth.logout(request)

	data = {
		'code': 0,
		'msg': 'Success'
	}
	return JsonResponse(data)