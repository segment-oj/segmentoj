from django.shortcuts import render
from problem.models import Problem
import markdown

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
	problem.description = markdown.markdown(
		problem.description,
		extensions=[
        	'markdown.extensions.extra',
        	'markdown.extensions.codehilite',
        ]
	)
	context['problem'] = problem
	return render(request, 'problemshow.html', context)