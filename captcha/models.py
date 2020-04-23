from django.db import models
from django.utils import timezone

import captcha.tools as tools

# Create your models here.
class CaptchaStore(models.Model):
	key = models.IntegerField()
	answer = models.CharField(max_length=10)
	expire_time = models.DateTimeField(default=tools.settimelater())

	@classmethod
	def clean_expire(self):
		self.objects.filter(expire_time__lte=timezone.now()).delete()