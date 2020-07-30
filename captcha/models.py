from django.db import models
from django.utils import timezone
from django.conf import settings

import captcha.tools as tools

# Create your models here.
class CaptchaStore(models.Model):
	key = models.IntegerField()
	answer = models.CharField(max_length=10)
	added_time = models.DateTimeField(auto_now=True)

	@classmethod
	def clean_expire(self):
		import os

		expired_data = self.objects.filter(added_time__gte=tools.settimelater(timezone.now()))
		for edata in expired_data:
			path = os.path.join(settings.BASE_DIR, "uploads", "captcha", "{name}.png".format(name=edata.key))
			os.remove(path)

			edata.delete()