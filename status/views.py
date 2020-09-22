from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from segmentoj import tools
from .models import Status, StatusDetail
from .serializers import StatusSerializer, StatusListSerializer
from problem.models import Problem
from segmentoj.decorator import login_required, syllable_required, parameter_required

# Create your views here.
class StatusView(APIView):
    @method_decorator(parameter_required("sid"))
    def get(self, request, sid):
        status_element = get_object_or_404(Status, id=sid)
        ss = StatusSerializer(status_element)

        return Response({"res": ss.data}, status=status.HTTP_200_OK)

    @method_decorator(syllable_required("problem", int))
    @method_decorator(syllable_required("code", str))
    @method_decorator(login_required())
    def post(self, request):
        # Create Status(Submit Problem)

        data = request.data
        data["owner"] = request.user.id

        if not data.get("lang"):
            data["lang"] = request.user.lang

        data["problem"] = get_object_or_404(Problem, pid=data["problem"]).id

        # Disallow User Provide These Syllables To Get not-judged AC
        data.pop("state", None)
        data.pop("time", None)
        data.pop("memory", None)
        data.pop("judge_detail", None)
        data.pop("add_time", None)
        data.pop("score", None)

        ss = StatusSerializer(data=data)
        ss.is_valid(raise_exception=True)
        ss.save()

        request.user.submit_time += 1
        return Response(status=status.HTTP_201_CREATED)


class StatusListView(APIView):
    def get(self, request):
        # Status List

        def process(x):
            problem = Problem.objects.get(id=x["problem"])
            x["problem"] = problem.pid
            return x

        status_filter = {}
        data = request.GET

        if data.get("problem"):
            status_filter["problem"] = Problem.objects.get(pid=data.get("problem")).id

        queryset = Status.objects.filter(**status_filter).order_by("-add_time")

        pg = LimitOffsetPagination()
        statuses = pg.paginate_queryset(queryset=queryset, request=request, view=self)

        ss = StatusListSerializer(statuses, many=True)
        return Response({"count": queryset.count(), "res": [process(x) for x in ss.data]}, status=status.HTTP_200_OK)


class StatusListCountView(APIView):
    def get(self, request):
        # Status List Count

        status_filter = {}
        data = request.GET

        queryset = Status.objects.filter(**status_filter).order_by("-add_time")
        res = queryset.count()

        return Response({"res": res}, status=status.HTTP_200_OK)
