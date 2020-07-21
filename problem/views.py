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
from .serializers import ProblemSerializer, ProblemListSerializer, TagSerializer
from segmentoj.decorator import syllable_required
from status.models import Status

class ProblemView(APIView):
    
    @method_decorator(syllable_required('pid', is_get_request=True))
    def get(self, request):
        # Get the content of a problem

        data = request.GET
        id = data.get('pid')
        if type(id) != int:
            id = int(id)

        problem = get_object_or_404(Problem, pid=id)

        if not problem.enabled and not request.user.has_perm('problem.view_hidden'):
            return Response({'detail': 'Problem is hidden.'}, status=status.HTTP_403_FORBIDDEN)
        
        ps = ProblemSerializer(problem)

        return Response(ps.get_problem(), status=status.HTTP_200_OK)

    @method_decorator(permission_required('problem.add_problem', raise_exception=True))
    def post(self, request):
        # Add a new problem

        data = request.data

        ps = ProblemSerializer(data=data)
        ps.is_valid(raise_exception=True)
        ps.save()
        return Response(status=status.HTTP_201_CREATED)

    @method_decorator(syllable_required('pid', int))
    @method_decorator(permission_required('problem.change_problem', raise_exception=True))
    def patch(slef, request):
        data = request.data
        id = data.get('pid')

        problem = get_object_or_404(Problem, pid=id)
        ps = ProblemSerializer(problem, data=data, partial=True)
        ps.is_valid(raise_exception=True)
        ps.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @method_decorator(syllable_required('pid', int))
    @method_decorator(permission_required('problem.delete_problem'))
    def delete(self, request):
        data = request.data
        id = data.get('pid')

        problem = get_object_or_404(Problem, pid=id)
        problem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagView(APIView):

    @method_decorator(syllable_required('id', int))
    def get(self, request):
        # Get a tag

        data = request.data
        id = data.get('id')

        tag = get_object_or_404(Tag, id=id)
        ts = TagSerializer(tag)

        return Response(ts.data, status=status.HTTP_200_OK)

    @method_decorator(permission_required('problem.add_tag', raise_exception=True))
    def post(self, request):
        # add new tag
        data = request.data
        ts = TagSerializer(data=data)
        ts.is_valid(raise_exception=True)
        tag = ts.save()

        return Response({
            'res': {
                'id': tag.id
            }
        }, status=status.HTTP_201_CREATED)

    @method_decorator(syllable_required('id', int))
    @method_decorator(permission_required('problem.delete_tag', raise_exception=True))
    def delete(self, request):
        # delete a tag
        data = request.data
        id = data.get('id')

        tag = get_object_or_404(Tag, id=id)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProblemListView(APIView):

    def get(self, request):
        def process_data(x):
            pid = x.get('pid')
            userid = request.user.id

            statusset = Status.objects.filter(problem=pid, owner=userid)
            if statusset.count() == 0:
                x['score'] = -1
            else:
                x['score'] = statusset.aggregate(Max('score'))['score__max']

            return x

        problem_filter = {}
        data = request.GET

        if not request.user.has_perm('problem.view_hidden'):
            problem_filter['enabled'] = True

        if data.get('title'):
            problem_filter['title__icontains'] = data.get('title')
        
        queryset = Problem.objects.filter(**problem_filter).order_by('pid')

        pg = LimitOffsetPagination()
        problems = pg.paginate_queryset(queryset=queryset, request=request, view=self)

        ps = ProblemListSerializer(problems, many=True)
        return Response({
            'res': [process_data(x) for x in ps.data]
        }, status=status.HTTP_200_OK)

class ProblemListCountView(APIView):

    def get(self, request):

        problem_filter = {}
        data = request.GET

        if not request.user.has_perm('problem.view_hidden'):
            problem_filter['enabled'] = True

        if data.get('title'):
            problem_filter['title__icontains'] = data.get('title')
        
        queryset = Problem.objects.filter(**problem_filter)
        res = queryset.count()
        return Response({
            'res': res
        }, status=status.HTTP_200_OK)