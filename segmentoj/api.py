# api request response code
from django.contrib import auth
from django.http import JsonResponse
import json
from . import tools

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

def register_api(request):
	data = json.loads(request.body)
	
	username = data['username']
	password = data['password']
	email = data['email']

	if not tools.isEmail(email):
		data = {
			'code': 1,
			'msg': 'Email address is not valid'
		}

		return JsonResponse(data)
	
	if len(password) < 6:
		data = {
			'code': 2,
			'msg': 'Password is too short'
		}

		return JsonResponse(data)

	if username == '':
		data = {
			'code': 3,
			'msg': 'Username is required'
		}

		return JsonResponse(data)

	user = auth.models.User.objects.create_user(username=username, password=password, email=email)

	if user:
		# Success
		user.save()
		data = {
			'code': 0,
			'msg': 'Success'
		}
		return JsonResponse(data)
	else:
		# failed
		data = {
			'code': 3,
			'msg': 'Failed to create user'
		}

		return JsonResponse(data)
