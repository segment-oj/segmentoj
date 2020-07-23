from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

import segmentoj.tools


def welcome(request):
    return HttpResponseRedirect("/admin")
