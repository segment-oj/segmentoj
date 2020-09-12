from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status

from .captchas import setcaptcha

# Create your views here.
def getcaptcha(request, key):
    setcaptcha(key)
    return redirect("/media/captcha/{name}.png".format(name=key))
