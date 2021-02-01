from rest_framework.response import Response
from rest_framework import status


def password_verification_required():
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            cur_passworld = request.data.get('current_password')

            if not cur_passworld:
                return Response({
                    'detail': 'Password verification required before accessing to target API'
                }, status=status.HTTP_403_FORBIDDEN)

            if not request.user.check_password(cur_passworld):
                return Response({
                    'detail': 'Invalid password.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
