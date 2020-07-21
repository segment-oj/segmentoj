from rest_framework.response import Response
from rest_framework import status

def syllable_required(syllable_id, syllable_type=None, is_get_request=False):
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            data = request.GET if is_get_request else request.data

            r = data.get(syllable_id)
            if r == None:
                return Response({
                    'detail': 'syllable {sid} is required'.format(sid=syllable_id)
                }, status=status.HTTP_400_BAD_REQUEST)

            if syllable_type != None and type(r) != syllable_type:
                return Response({
                    'detail': 'syllable {sid} has wrong type'.format(sid=syllable_id)
                }, status=status.HTTP_400_BAD_REQUEST)

            return func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def login_required():
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response({
                    'detail': 'Login Required'
                }, status=status.HTTP_401_UNAUTHORIZED)

            return func(request, *args, **kwargs)
        return _wrapped_view
    return decorator