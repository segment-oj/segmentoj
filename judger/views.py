from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import requests
import secrets

from segmentoj.decorator import parameter_required, syllable_required
from status.models import Status
from problem.models import Problem
from .decorator import judger_account_required
from .serializers import StatusSerializer, StatusEditSerializer, ProblemSerializer

# Create your views here.


class JudgerTaskView(APIView):
    @method_decorator(judger_account_required())
    @method_decorator(parameter_required('tid'))
    def get(self, request, tid):
        status_element = get_object_or_404(Status, id=tid)
        ss = StatusSerializer(status_element)
        ss_data = ss.data
        ss_data['problem'] = status_element.problem.pid

        return Response({'res': ss_data}, status=status.HTTP_200_OK)

    @method_decorator(judger_account_required())
    @method_decorator(parameter_required('tid'))
    def patch(self, request, tid):
        data = request.data
        problem = get_object_or_404(Status, id=tid)
        ps = StatusEditSerializer(problem, data=data, partial=True)
        ps.is_valid(raise_exception=True)
        ps.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JudgerProblemView(APIView):
    @method_decorator(parameter_required('pid'))
    @method_decorator(judger_account_required())
    def get(self, request, pid):
        # Get the content of a problem
        problem = get_object_or_404(Problem, pid=pid)

        ps = ProblemSerializer(problem)
        return Response({'res': ps.data}, status=status.HTTP_200_OK)


class JudgerTokenView(APIView):
    @method_decorator(judger_account_required())
    def get(self, request):
        token = secrets.token_urlsafe(64)

        try:
            res = requests.post('{base_url}/api/token'.format(base_url=settings.JUDGER_PORT['base_url']), json={
                'token': token,
                'password': settings.JUDGER_PORT.get('password'),
            })
            res_json = res.json()
        except:
            return Response({
                'detail': 'Cannot connect to judger port.',
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            code = res_json.get('code')

            if code is None:
                return Response({
                    'detail': 'Judger Port response format incorrect.'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            elif code == 4004:
                return Response({
                    'detail': 'Judger Port don\'t understand our format.\n'
                    'Maybe an upgrade is required.'
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({
            'code': 1000,
            'res': token,
        }, status=status.HTTP_200_OK)
