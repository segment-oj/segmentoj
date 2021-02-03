from django.db import models
from django.db.models import indexes
from django.db.models.base import Model

# Create your models here.
class Tag(models.Model):
    content = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=30, default="blue")

    def __str__(self):
        return self.content

class Problem(models.Model):
    pid = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    
    allow_html = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)

    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=128000)

    testdata_url = models.TextField(blank=True, null=True)

    class Meta:
        permissions = ( # (permission name, promission explanation)
            ('view_hidden', 'Can view hidden problem'),
        )

        indexes = [
            models.Index(fields=['pid']),
            models.Index(fields=['title']),
        ]

    def __str__(self):
        return self.title

