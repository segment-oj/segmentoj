from django.db import models

# Create your models here.
class Tag(models.Model):
	content = models.CharField(max_length=30, unique=True)
	color = models.CharField(max_length=30, default="blue")

	def __str_(self):
		return self.content

class Problem(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()

	show_id = models.IntegerField(unique=True)
	date_added = models.DateTimeField(auto_now_add=True)
	allow_html = models.BooleanField(default=False)
	enabled = models.BooleanField(default=True)
	tags = models.ManyToManyField(Tag, null=True, blank=True)

	def getTags(self):
		return self.tags.all()

	def __str_(self):
		return self.title

