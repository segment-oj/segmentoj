from django.shortcuts import render
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from status import JudgeStatus as js
from status.models import Status, StatusDetail
from .decorator import judger_account_required
from .serializers import StatusSerializer, StatusDetailSerializer
from segmentoj.decorator import parameter_required, syllable_required

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

class JudgerStatusDetailView(APIView):

    @method_decorator(judger_account_required())
    @method_decorator(parameter_required("sid"))
    def get(self, request, sid, cid=None):
        res_status = Status.objects.get(id=sid)
        ss = StatusSerializer(res_status)
        return Response({
            "res": ss.data
        }, status=status.HTTP_200_OK)

    @method_decorator(judger_account_required())
    @method_decorator(parameter_required("sid"))
    @method_decorator(parameter_required("cid"))
    @method_decorator(syllable_required("state", int))
    def post(self, request, sid, cid):
        data = request.data
        data["caseid"] = cid
        data["main_status"] = sid
        res_status = Status.objects.get(id=sid)
        
        try:
            res_detail_set = res_status.judge_detail.get(caseid=cid)
        except StatusDetail.DoesNotExist:
            res_detail_set = None
        
        ss = StatusDetailSerializer(res_detail_set, data, partial=True)
        ss.is_valid(raise_exception=True)
        ss.save()
        return Response(status=status.HTTP_201_CREATED)
