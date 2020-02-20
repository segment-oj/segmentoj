from django.db import models
from django.contrib.auth.models import User
from soj.storage import AvatarStorage

from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class account(models.Model):
	uid = models.IntegerField()
	to_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')

	avatar = models.FileField(upload_to="avatar", storage=AvatarStorage(uid))
	solved = models.IntegerField(default=0)
	submit_time = models.IntegerField(default=0)

	def __str__(self):
		return str(self.uid)

@receiver(post_save,sender=User)
def create_user_extension(sender,instance,created,**kwargs):
    if created:
        account.objects.create(to_user=instance, uid=instance.id)
    else:
        instance.account.save()