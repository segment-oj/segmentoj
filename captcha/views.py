from django.http import HttpResponse
from .captchas import set_captcha

# Create your views here.
def get_captcha(request, key):
    return HttpResponse(set_captcha(key), content_type='image/png')
