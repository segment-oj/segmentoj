from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status

from .captchas import set_captcha

# Create your views here.
def get_captcha(request, key):
    set_captcha(key)
    return redirect("/media/captcha/{name}.png".format(name=key))
