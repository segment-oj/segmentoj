from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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
        status = get_object_or_404(Status, id=tid)
        ss = StatusSerializer(status)
        return Response({
            'code': 1000,
            'res': ss.data,
        }, status=status.HTTP_200_OK)

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

