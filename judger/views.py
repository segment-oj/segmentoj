from django.shortcuts import render
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from status import JudgeStatus as js
from status.models import Status
from .decorator import judger_account_required

# Create your views here.
class JudgerStatusView(APIView):

    @method_decorator(judger_account_required())
    def get(self, request):
        task_filter = {"state": js.JUDGE_STATUS_WAITING}
        queryset = Status.objects.filter(**task_filter).order_by("id")[:1]
        res_status = queryset[0]
        res_status.state = js.JUDGE_STATUS_INPROCESS

        return Response({
            "res": res_status.id
        }, status=status.HTTP_200_OK)
