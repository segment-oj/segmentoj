from django.shortcuts import render

def welcome(request):
	context = {}
	return render(request, 'welcome.html', context)