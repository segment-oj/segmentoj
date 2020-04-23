# public function to use
from django.conf import settings
import os

from captcha.tools import GenCaptcha, settimelater
from captcha.models import CaptchaStore

def setcaptcha(key):
	g = GenCaptcha()
	path = os.path.join(settings.BASE_DIR, \
		"uploads", "captcha", "${name}.png".format(name=key))

	ans = g.createImg(path)

	s = CaptchaStore(key=key, answer=ans, expire_time=settimelater())
	s.save()
	return ans
	