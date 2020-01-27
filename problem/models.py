from django.db import models

# Create your models here.
class Problem(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	background = models.TextField()
	sampleinput = models.TextField()
	sampleoutput = models.TextField()

	show_id = models.IntegerField()
	date_added = models.DateTimeField(auto_now_add=True)

	def __str_(self):
		return self.title