from rest_framework.response import Response
from rest_framework import status

def syllable_required(syllable_id, syllable_type=None):
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            r = request.data.get(syllable_id)
            if r == None:
                return Response({
                    'detail': 'syllable {sid} is required'.format(sid=syllable_id)
                }, status=status.HTTP_400_BAD_REQUEST)

            if syllable_type != None and type(r) != syllable_type:
                return Response({
                    'detail': 'syllable {sid} has wrong type'.format(sid=syllable_id)
                })

            return func(request, *args, **kwargs)
        return _wrapped_view
    return decorator