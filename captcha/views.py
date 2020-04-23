from django.shortcuts import redirect

from . import captcha

# Create your views here.
def getcaptcha(request, key):
	captcha.setcaptcha(key)
	return redirect("/media/captcha/{name}.png".format(name=key))