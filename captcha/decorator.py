from rest_framework.response import Response
from rest_framework import status

from captcha.captchas import check


def captcha_required():
    def decorator(func):
        def _wrapped_view(request, *args, **kwargs):
            data = request.data

            captcha_key = data.get("cpatcha_key")
            captcha_asnwer = data.get("captcha_answer")

            if captcha_key == None or captcha_asnwer == None:
                return Response({
                    "detail": "Captcha is required"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if check(captcha_key, captcha_asnwer):
                return Response({
                    "detail": "Captcha wrong"
                }, status=status.HTTP_406_NOT_ACCEPTABLE)

            return func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
