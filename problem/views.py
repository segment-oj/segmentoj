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