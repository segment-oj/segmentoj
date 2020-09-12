from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status

from .captchas import setcaptcha

# Create your views here.

def getcaptcha(request, key):
    if not str(key).isdigit():
        return Response({
            "detail": "Only digit is allow in captcha key"
        }, status=status.HTTP_400_BAD_REQUEST)

    setcaptcha(key)
    return redirect("/media/captcha/{name}.png".format(name=key))
