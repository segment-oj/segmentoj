from django.db import models
from problem import models as pm
from soj.storage import AvatarStorage

# Create your models here.
class account(models.Model):
	to_user = models.OneToOneField(pm.Problem, on_delete=models.CASCADE)

	avatar = models.FileField(upload_to="avatar", storage=AvatarStorage(to_user.id))
	solved = models.IntegerField(default=0)
	submit_time = models.IntegerField(default=0)
