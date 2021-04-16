from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Account(AbstractUser):
    introduction = models.TextField(blank=True, null=True, default="# Hello World!")
    lang = models.TextField(default='cxx;17,clang,O2')
    solved = models.IntegerField(default=0)
    submit_time = models.IntegerField(default=0)

    avatar_url = models.TextField(blank=True, null=True)

    extra_data = models.TextField(blank=True, null=True)

    first_name = None  # delete unused field
    last_name = None  # delete unused field

    is_judger = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
