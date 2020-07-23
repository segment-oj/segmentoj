from account.models import User
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from segmentoj import tools
from segmentoj.decorator import syllable_required

# Create your views here.
