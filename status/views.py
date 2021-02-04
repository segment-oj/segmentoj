from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from .models import Status
from .serializers import StatusSerializer, StatusListSerializer
from problem.models import Problem
from segmentoj.decorator import login_required, syllable_required, parameter_required
from . import JudgeLang as JLang
from . import JudgeState as JState

import requests

# Create your views here.
class StatusView(APIView):
    @method_decorator(parameter_required('sid'))
    def get(self, request, sid):
        status_element = get_object_or_404(Status, id=sid)
        ss = StatusSerializer(status_element)
        ss_data = ss.data
        ss_data['problem'] = status_element.problem.pid

        return Response({'res': ss_data}, status=status.HTTP_200_OK)

    @method_decorator(syllable_required('problem', int))
    @method_decorator(syllable_required('code', str))
    @method_decorator(syllable_required('lang', int))
    @method_decorator(login_required())
    def post(self, request):
        # Create Status(Submit Problem)

        data = request.data

        if 1 <= data['lang'] <= 10:
            return Response({
                'code': 4001,
                'detail': 'Unknow language',
            })

        builder = {}
        builder['owner'] = request.user.id
        builder['lang'] = data['lang']
        builder['code'] = data['code']

        if data.get('lang_info') is None:
            builder['lang_info'] = JLang.DEFAULT_LANG_INFO[data['lang']]
        else:
            builder['lang_info'] = data.get('lang_info')

        builder['problem'] = get_object_or_404(Problem, pid=data['problem']).id

        ss = StatusSerializer(data=builder)
        ss.is_valid(raise_exception=True)
        status_element = ss.save()

        request.user.submit_time += 1
        request.user.save()

        def cannot_judge(reason, state=JState.JUDGE_STATUS_CFGE):
            status_element.state = state
            status_element.additional_info = reason
            status_element.save()

        try:
            res = requests.post('{base_url}/api/task'.format(base_url=settings.JUDGER_PORT['base_url']), json={
                'task_id': status_element.id,
                'password': settings.JUDGER_PORT.get('password'),
            })
            res_json = res.json()
        except:
            cannot_judge('Cannot connect the Judger Port.')
        else:
            code = res_json.get('code')

            if code is None:
                cannot_judge('Judger Port response format incorrect.', JState.JUDGE_STATUS_SE)
            elif code == 3003 or code == 3001:
                cannot_judge('Judger Port refused our task.')
            elif code == 2001:
                cannot_judge('No judger connected to Judger Port.', JState.JUDGE_STATUS_SE)

        return Response({
            'id': status_element.id
        }, status=status.HTTP_201_CREATED)


class StatusListView(APIView):
    def get(self, request):
        # Status List

        def process(x):
            problem = Problem.objects.get(id=x['problem'])
            x['problem'] = problem.pid
            return x

        status_filter = {}
        data = request.GET

        if type(data.get('problem')) == int:
            status_filter['problem'] = get_object_or_404(Problem, pid=data['problem']).id

        if data.get('lang') is not None:
            status_filter['lang'] = data['lang']

        if data.get('owner') is not None:
            status_filter['owner'] = data['owner']

        if data.get('score') is not None:
            status_filter['score'] = data['score']

        queryset = Status.objects.filter(**status_filter).order_by('-add_time')

        pg = LimitOffsetPagination()
        statuses = pg.paginate_queryset(queryset=queryset, request=request, view=self)

        ss = StatusListSerializer(statuses, many=True)
        return Response({'count': queryset.count(), 'res': [process(x) for x in ss.data]}, status=status.HTTP_200_OK)
