from django.db import models

from account.models import User
from problem.models import Problem

from . import JudgeStatus

# Create your models here.
class Status(models.Model):
    state = models.IntegerField(default=0)

    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    lang = models.IntegerField(default=0)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    code = models.TextField()

    add_time = models.DateTimeField(auto_now_add=True)

    def fresh_state(self):
        for Jdetail in self.judge_detail:
            if Jdetail.state < 10:
                self.state = Jdetail.state
                return
        
        for Jdetail in self.judge_detail:
            if Jdetail.state >= 20:
                self.state = Jdetail.state
                return

        self.state = self.judge_detail[0].state

    def __str__(self):
        return str(self.id)

class StatusDetail(models.Model):
    state = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)

    input_s = models.CharField(max_length=100)
    output_s = models.CharField(max_length=100)
    answer_s = models.CharField(max_length=100)
    main_state = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='judge_detail')