from django.db import models
from mdeditor.fields import MDTextField

# Create your models here.
class Problem(models.Model):
	title = models.CharField(max_length=100)
	description = MDTextField()

	show_id = models.IntegerField()
	date_added = models.DateTimeField(auto_now_add=True)

	def __str_(self):
		return self.title