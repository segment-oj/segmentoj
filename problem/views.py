from django.shortcuts import render, get_object_or_404
from django.http import Http404

from problem.models import Problem
import markdown
import html

# Create your views here.

def problemlist(request):
	context = {}
	problemlist = Problem.objects.order_by('show_id')
	context['problems'] = problemlist
	return render(request, 'problemlist.html', context)

def problemshow(request, pid):
	context = {}
	problem = get_object_or_404(Problem, show_id=pid)

	if not problem.enabled and not request.user.is_superuser:
		raise Http404

	if not problem.allow_html:
		problem.description = html.escape(problem.description)

	problem.description = markdown.markdown(
		problem.description,
		extensions=[
        	'markdown.extensions.extra',
        	'markdown.extensions.codehilite',
        ]
	)
	context['problem'] = problem
	context['tags'] = problem.getTags()
	return render(request, 'problemshow.html', context)