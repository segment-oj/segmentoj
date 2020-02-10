from django.shortcuts import render

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