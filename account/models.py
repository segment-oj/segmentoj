from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    USERNAME_FIELD = "username"
    email = models.EmailField()

    introduction = models.TextField(blank=True, null=True, default="# Hello World!")
    lang = models.IntegerField(default=0)
    solved = models.IntegerField(default=0)
    submit_time = models.IntegerField(default=0)

    def __str__(self):
        return self.username
