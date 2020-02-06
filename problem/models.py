from django.db import models

# Create your models here.
class Problem(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()

	show_id = models.IntegerField(unique=True)
	date_added = models.DateTimeField(auto_now_add=True)
	allow_html = models.BooleanField(default=False)

	def __str_(self):
		return self.title