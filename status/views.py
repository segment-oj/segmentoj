from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.pagination import LimitOffsetPagination

from segmentoj import tools
from .models import Status, StatusDetail
from .serializers import StatusSerializer
from problem.models import Problem
from segmentoj.decorator import login_required, syllable_required

# Create your views here.
class StatusView(APIView):

    @method_decorator(syllable_required('id', int))
    def get(self, request):
        data = request.data

        id = data.get('id')
        status = get_object_or_404(Status, id=id)
        ss = StatusSerializer(status)

        return Response({
            'res': ss.data
        }, status=HTTP_200_OK)

    @method_decorator(syllable_required('problem', int))
    @method_decorator(syllable_required('code', str))
    @method_decorator(login_required())
    def post(self, request):
        # Create Status(Submit Problem)

        data = request.data
        data['owner'] = request.user.id

        if not data.get('lang'):
            data['lang'] = request.user.lang
        
        data['problem'] = get_object_or_404(Problem, pid=data['problem']).id
        
        # Disallow User Provide These Syllables To Get Unjudged AC
        data.pop('state', None)
        data.pop('time', None)
        data.pop('memory', None)
        data.pop('judge_detail', None)
        data.pop('add_time', None)
        data.pop('score', None)

        ss = StatusSerializer(data=data)
        ss.is_valid(raise_exception=True)
        ss.save()
        return Response(status=HTTP_201_CREATED)

