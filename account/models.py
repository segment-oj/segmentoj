from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(AbstractUser):
    introduction = models.TextField(blank=True, null=True, default="# Hello World!")
    lang = models.IntegerField(default=0)
    solved = models.IntegerField(default=0)
    submit_time = models.IntegerField(default=0)

    list_column = models.IntegerField(default=20)
    nav_color = models.TextField(default="#545c64")
    editor_theme = models.IntegerField(default=0)

    first_name = None # delete unused feild
    last_name = None # delete unused feild

    is_judger = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
