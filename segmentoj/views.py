from django.shortcuts import render
from problem.models import Problem

def welcome(request):
	context = {}
	return render(request, 'welcome.html', context)

def problemlist(request):
	context = {}
	problemlist = Problem.objects.order_by('show_id')
	context['problems'] = problemlist
	return render(request, 'problemlist.html', context)

def problemshow(request, pid):
	context = {}
	problem = Problem.objects.get(show_id=pid)
	context['problem'] = problem
	return render(request, 'problemshow.html', context)