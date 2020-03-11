from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import soj.models
import segmentoj.tools

def welcome(request):
	context = {}
	return render(request, 'welcome.html', context)

def login(request):
	context = {}
	return render(request, 'user/login.html', context)

def logout(request):
	context = {}
	return render(request, 'user/logout.html', context)

def register(request):
	context = {}
	return render(request, 'user/register.html', context)

def show_user(request, uid):
	context = {}
	user = get_object_or_404(User, id=uid)
	account = user.account

	account.home = segmentoj.tools.markdown2html(
		account.home
	)

	context['account'] = account
	return render(request, 'user/show_home.html', context)
