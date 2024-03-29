import json
from re import sub
import time

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
from segmentoj.decorator import login_required, syllable_required, parameter_required, parse_as_integer
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
        problem = get_object_or_404(Problem, pid=data['problem'])

        # Build status
        if not 1 <= data['lang'] <= 10:
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

        builder['problem'] = problem.id

        ss = StatusSerializer(data=builder)
        ss.is_valid(raise_exception=True)
        status_element = ss.save()

        # User statistic update
        request.user.submit_time += 1

        submit_list = json.loads(request.user.submit_list)
        if submit_list.count(data['problem']) == 0:
            submit_list.append(data['problem'])
        request.user.submit_list = json.dumps(submit_list)

        submit_heatmap = json.loads(request.user.submit_heatmap)
        localtime = time.localtime(time.time())
        submit_heatmap[localtime.tm_mon -
                       1]["data"][localtime.tm_mday - 1] += 1
        request.user.submit_heatmap = json.dumps(submit_heatmap)

        request.user.save()

        # Problem statistic update
        problem.submit_cnt += 1
        problem.save()

        def cannot_judge(reason, state=JState.JUDGE_STATUS_CFGE):
            status_element.state = state
            status_element.additional_info = reason
            status_element.save()

        # Judger Port
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
                cannot_judge('Judger Port response format incorrect.',
                             JState.JUDGE_STATUS_SE)
            elif code == 3003 or code == 3001:
                cannot_judge('Judger Port refused our task.')
            elif code == 2001:
                cannot_judge('No judger connected to Judger Port.',
                             JState.JUDGE_STATUS_SE)

        return Response({
            'id': status_element.id
        }, status=status.HTTP_201_CREATED)


class StatusListView(APIView):

    @method_decorator(parse_as_integer('problem'))
    @method_decorator(parse_as_integer('lang'))
    @method_decorator(parse_as_integer('owner'))
    def get(self, request):
        # Status List

        def process(x):
            problem = Problem.objects.get(id=x['problem'])
            x['problem'] = problem.pid
            return x

        status_filter = {}
        data = request.GET

        if data.get('problem') is not None:
            status_filter['problem'] = get_object_or_404(
                Problem, pid=data['problem']).id

        if data.get('lang') is not None:
            status_filter['lang'] = data['lang']

        if data.get('owner') is not None:
            status_filter['owner'] = data['owner']

        queryset = Status.objects.filter(**status_filter).order_by('-id')

        pg = LimitOffsetPagination()
        statuses = pg.paginate_queryset(
            queryset=queryset, request=request, view=self)

        ss = StatusListSerializer(statuses, many=True)
        return Response({'count': queryset.count(), 'res': [process(x) for x in ss.data]}, status=status.HTTP_200_OK)
