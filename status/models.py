from django.db import models

from account.models import User
from problem.models import Problem

from . import JudgeStatus

# Create your models here.
class Status(models.Model):
    score = models.IntegerField(default=0)
    state = models.IntegerField(default=0)

    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    lang = models.IntegerField(default=0)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    code = models.TextField()

    add_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        index_together = ["owner", "problem"]


class StatusDetail(models.Model):
    state = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)

    input_s = models.CharField(max_length=100, null=True, blank=True)
    output_s = models.CharField(max_length=100, null=True, blank=True)
    error_s = models.CharField(max_length=100, null=True, blank=True)
    answer_s = models.CharField(max_length=100, null=True, blank=True)

    caseid = models.IntegerField()
    main_status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name="judge_detail"
    )

