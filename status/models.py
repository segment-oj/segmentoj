from django.db import models

from account.models import Account
from problem.models import Problem
from . import JudgeState as JState

# Create your models here.
class Status(models.Model):
    score = models.IntegerField(default=0)
    state = models.IntegerField(default=JState.JUDGE_STATUS_WAITING)

    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)

    # Language
    lang = models.IntegerField() # Major language
    lang_info = models.CharField(max_length=25, blank=True, null=True) # Detail Compiler Infomation

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='status')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    # Judger
    judge_by = models.ForeignKey(Account, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='judged_status')
    judge_time = models.DateTimeField(blank=True, null=True)

    code = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    # Judge detail info of each testcases
    detail = models.TextField(blank=True, null=True)

    # Additional infomation provided by judger
    additional_info = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return '[{id}] {owner}'.format(id=self.id, title=self.owner.username)

    class Meta:
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['score']),
            models.Index(fields=['lang']),
            models.Index(fields=['problem', 'owner']),
        ]
