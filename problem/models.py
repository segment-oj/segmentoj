from django.db import models

# Create your models here.
class Tag(models.Model):
	content = models.CharField(max_length=30, unique=True)
	color = models.CharField(max_length=30, default="blue")

	def __str__(self):
		return self.content

class Problem(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()

	pid = models.IntegerField(unique=True)
	date_added = models.DateTimeField(auto_now_add=True)
	allow_html = models.BooleanField(default=False)
	enabled = models.BooleanField(default=True)
	tags = models.ManyToManyField(Tag, blank=True)

    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=128000)

	class Meta:
		permissions = ( # (permission name, promission explaination)
			('view_hidden', 'Can view hidden problem'),
        )

	def getTags(self):
		return self.tags.all()

	def __str__(self):
		return self.title

