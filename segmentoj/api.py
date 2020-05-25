# api request response code
from django.contrib import auth
from django.http import JsonResponse
import json
from . import tools
from captcha import captcha

def login_api(request):
	data = json.loads(request.body)

	username = data['username']
	password = data['password']

	user = auth.authenticate(request,username=username,password=password)

	if user:
		# authenticate success
		auth.login(request,user);
		res = {
			'code': 20,
			'msg': "Login Success"
		}

		return JsonResponse(res)
	else:
		# failed
		res = {
			'code': 41,
			'msg': 'Username or password wrong, authenticate failed.'
		}

		return JsonResponse(res)

def logout_api(request):
	if not request.user.is_authenticate():
		res = {
			'code': 42,
			'msg': 'Not logged in.'
		}

		return JsonResponse(res);

	auth.logout(request)

	res = {
		'code': 20,
		'msg': 'Success'
	}
	return JsonResponse(res)

def register_api(request):
	data = json.loads(request.body)
	
	username = data['username']
	password = data['password']
	email = data['email']

	try:
		ckey = data['captcha-key']
		canswer = data['captcha-ans']
	except KeyError:
		res = {
			'code': 31,
			'msg': 'Captcha is required'
		}

		return JsonResponse(res)
	
	if (not captcha.check(ckey, canswer)):
		res = {
			'code': 32,
			'msg': 'Captcha is incorrect'
		}

		return JsonResponse(res)

	if email != '' and not tools.isEmail(email):
		res = {
			'code': 11,
			'msg': 'Email address is not valid'
		}

		return JsonResponse(res)
	
	if len(password) < 6:
		res = {
			'code': 11,
			'msg': 'Password is too short'
		}

		return JsonResponse(res)

	if username == '':
		res = {
			'code': 11,
			'msg': 'Username is required'
		}

		return JsonResponse(res)

	user = auth.models.User.objects.create_user(username=username, password=password, email=email)

	if user:
		# Success
		user.save()
		res = {
			'code': 20,
			'msg': 'Success'
		}
		return JsonResponse(res)
	else:
		# failed
		data = {
			'code': 15,
			'msg': 'Failed to create user'
		}

		return JsonResponse(res)
