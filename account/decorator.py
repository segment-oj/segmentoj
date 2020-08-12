from rest_framework.response import Response
from rest_framework import status


def password_verify_required(clear_storage=True):
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.session.get("password_verified"):
                return Response({
                    "detail": "Password Verify Required Before Access To This API"
                }, status=status.HTTP_403_FORBIDDEN)

            if clear_storage:
                request.session["password_verified"] = False
            
            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
