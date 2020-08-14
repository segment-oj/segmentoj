from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Max

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from segmentoj import tools
from problem.models import Problem, Tag
from .serializers import (
    ProblemSerializer,
    ProblemDescriptionSerializer,
    ProblemListSerializer,
    TagSerializer,
)
from segmentoj.decorator import (
    syllable_required,
    parameter_required,
)
from status.models import Status
from .decorator import view_hidden_problem_permission_required


class ProblemView(APIView):
    @method_decorator(parameter_required("pid"))
    @method_decorator(view_hidden_problem_permission_required())
    def get(self, request, pid):
        # Get the content of a problem
        problem = get_object_or_404(Problem, pid=pid)

        ps = ProblemSerializer(problem)
        return Response({"res": ps.data}, status=status.HTTP_200_OK)

    @method_decorator(permission_required("problem.add_problem", raise_exception=True))
    def post(self, request):
        # Add a new problem

        data = request.data

        ps = ProblemSerializer(data=data)
        ps.is_valid(raise_exception=True)
        ps.save()
        return Response(status=status.HTTP_201_CREATED)

    @method_decorator(parameter_required("pid"))
    @method_decorator(permission_required("problem.change_problem", raise_exception=True))
    def patch(self, request, pid):
        data = request.data

        problem = get_object_or_404(Problem, pid=pid)
        ps = ProblemSerializer(problem, data=data, partial=True)
        ps.is_valid(raise_exception=True)
        ps.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_decorator(permission_required("problem.delete_problem"))
    def delete(self, request, pid):
        data = request.data

        problem = get_object_or_404(Problem, pid=pid)
        problem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProblemDescriptionView(APIView):
    @method_decorator(parameter_required("pid"))
    @method_decorator(view_hidden_problem_permission_required())
    def get(self, request, pid):
        problem = get_object_or_404(Problem, pid=pid)

        pds = ProblemDescriptionSerializer(problem)
        return Response({"res": pds.data}, status=status.HTTP_200_OK)


class TagView(APIView):
    @method_decorator(parameter_required("tid"))
    def get(self, request, tid):
        # Get a tag
        tag = get_object_or_404(Tag, id=tid)
        ts = TagSerializer(tag)

        return Response({"res": ts.data}, status=status.HTTP_200_OK)

    @method_decorator(permission_required("problem.add_tag", raise_exception=True))
    def post(self, request):
        # add new tag
        data = request.data
        ts = TagSerializer(data=data)
        ts.is_valid(raise_exception=True)
        tag = ts.save()

        return Response({"res": {"id": tag.id}}, status=status.HTTP_201_CREATED)

    @method_decorator(parameter_required("tid"))
    @method_decorator(permission_required("problem.delete_tag", raise_exception=True))
    def delete(self, request, tid):
        # delete a tag
        data = request.data

        tag = get_object_or_404(Tag, id=tid)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProblemListView(APIView):
    def get(self, request):
        def process_data(x):
            pid = x.get("id")

            userid = request.user.id

            statusset = Status.objects.filter(problem=pid, owner=userid)
            if statusset.count() == 0:
                x["score"] = -1
            else:
                x["score"] = statusset.aggregate(Max("score"))["score__max"]

            x.pop("id")  # Don't Leake ID in DataBase
            return x

        problem_filter = {}
        data = request.GET

        if not request.user.has_perm("problem.view_hidden"):
            problem_filter["enabled"] = True

        if data.get("title"):
            problem_filter["title__icontains"] = data.get("title")

        queryset = Problem.objects.filter(**problem_filter).order_by("pid")

        pg = LimitOffsetPagination()
        problems = pg.paginate_queryset(queryset=queryset, request=request, view=self)

        ps = ProblemListSerializer(problems, many=True)
        return Response(
            {"count": queryset.count(), "res": [process_data(x) for x in ps.data]},
            status=status.HTTP_200_OK,
        )

class ProblemListCountView(APIView):
    def get(self, request):

        problem_filter = {}
        data = request.GET

        if not request.user.has_perm("problem.view_hidden"):
            problem_filter["enabled"] = True

        if data.get("title"):
            problem_filter["title__icontains"] = data.get("title")

        queryset = Problem.objects.filter(**problem_filter)
        res = queryset.count()
        return Response({"res": res}, status=status.HTTP_200_OK)

class TagListView(APIView):

    def get(self, request):
        queryset = Tag.objects.all()
        ts = TagSerializer(queryset, many=True)

        return Response({
            "detail": "Success",
            "count": queryset.count(),
            "res": ts.data
        }, status=status.HTTP_200_OK)