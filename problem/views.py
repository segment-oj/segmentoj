from django.shortcuts import render, get_object_or_404
from django.http import Http404

from problem.models import Problem
import segmentoj.tools

# Create your views here.

def problemlist(request):
	context = {}
	problemlist = Problem.objects.order_by('show_id')
	context['problems'] = problemlist

	if request.user.has_perm('problem.view_hidden'):
		context['viewhid'] = True
	else:
		context['viewhid'] = False

	return render(request, 'problemlist.html', context)

def problemshow(request, pid):
	context = {}
	problem = get_object_or_404(Problem, show_id=pid)

	if not problem.enabled and not request.user.has_perm("problem.view_hidden"):
		raise Http404

	problem.description = segmentoj.tools.markdown2html(
		problem.description,
		problem.allow_html
	)
	context['problem'] = problem
	context['tags'] = problem.getTags()
	return render(request, 'problemshow.html', context)