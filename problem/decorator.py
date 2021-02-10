from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from problem.models import Problem


def view_hidden_problem_permission_check():
    def decorator(func):
        def _wrapped_view(request, pid, *args, **kwargs):
            problem = get_object_or_404(Problem, pid=pid)

            if not problem.enabled and not request.user.has_perm('problem.view_hidden'):
                return Response(
                    {'detail': 'Problem is hidden.'}, status=status.HTTP_403_FORBIDDEN
                )

            return func(request, pid=pid, *args, **kwargs)

        return _wrapped_view

    return decorator
