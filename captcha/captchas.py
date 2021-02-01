# public function to use
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
import os.path

from captcha.tools import GenCaptcha
from captcha.models import CaptchaStore


def set_captcha(key):
    g = GenCaptcha()
    path_prefix = os.path.join(settings.BASE_DIR, "uploads", "captcha")
    path = os.path.join(path_prefix, "{name}.png".format(name=key))

    ans = g.createImg(path)

    try:
        # try to get if already there
        s = CaptchaStore.objects.get(key=key)
        s.answer = ans
        s.save()
    except ObjectDoesNotExist:
        # not exist, create new
        s = CaptchaStore(key=key, answer=ans)
        s.save()

    return ans


def check(key, ans):
    CaptchaStore.clean_expire()

    try:
        s = CaptchaStore.objects.get(key=key)
    except ObjectDoesNotExist:
        return False
    else:
        if s.answer == ans.lower():
            s.delete()
            return True
        else:
            s.delete()
            return False
