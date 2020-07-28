# public function to use
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import os

from captcha.tools import GenCaptcha, settimelater
from captcha.models import CaptchaStore

def setcaptcha(key):
	g = GenCaptcha()
	path = os.path.join(settings.BASE_DIR, \
		"uploads", "captcha", "{name}.png".format(name=key))

	ans = g.createImg(path)

	try:
		# try to get if already there
		s = CaptchaStore.objects.get(key=key)
		s.answer = ans
		s.expire_time = settimelater()
		s.save()
	except ObjectDoesNotExist:
		# not exist, create new
		s = CaptchaStore(key=key, answer=ans, expire_time=settimelater())
		s.save()
	
	return ans
	
def check(key, ans):
	CaptchaStore.clean_expire()

	try:
		s = CaptchaStore.objects.get(key=key)
	except ObjectDoesNotExist:
		return False
	else:
		if (s.answer == ans.lower()):
			s.delete()
			return True
		else:
			s.delete()
			return False