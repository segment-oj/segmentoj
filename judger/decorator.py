from rest_framework.response import Response
from rest_framework import status

def judger_account_required():
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {"detail": "Login Required"}, status=status.HTTP_401_UNAUTHORIZED
                )

            if not request.user.is_judger:
                return Response(
                    {"detail": "Judger Account Required"}, status=status.HTTP_403_FORBIDDEN
                )

            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
