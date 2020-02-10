from django.shortcuts import render

def welcome(request):
	context = {}
	return render(request, 'welcome.html', context)

def login(request):
	context = {}
	return render(request, 'login.html', context)

def logout(request):
	context = {}
	return render(request, 'logout.html', context)