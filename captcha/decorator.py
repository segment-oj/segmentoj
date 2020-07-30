from rest_framework.response import Response
from rest_framework import status

from captcha.captchas import check


def captcha_required():
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            data = request.data

            captcha_key = data.get("captcha_key")
            captcha_answer = data.get("captcha_answer")

            if captcha_key == None or captcha_answer == None:
                return Response({
                    "detail": "Captcha is required"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if check(captcha_key, captcha_answer):
                return Response({
                    "detail": "Captcha wrong"
                }, status=status.HTTP_406_NOT_ACCEPTABLE)

            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
