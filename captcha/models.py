from django.db import models
from django.utils import timezone
from django.conf import settings

from datetime import timedelta

# Create your models here.


class CaptchaStore(models.Model):
    key = models.IntegerField(unique=True)
    answer = models.CharField(max_length=10)
    added_time = models.DateTimeField(auto_now=True)

    @classmethod
    def clean_expire(self):
        self.objects.filter(
            added_time__lte=timezone.now() - timedelta(minutes=settings.CAPTCHA['age'])
        ).delete()
