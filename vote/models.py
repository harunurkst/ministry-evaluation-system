from django.db import models
from django.contrib.auth.models import User
from nid.models import NidInfo


class Ministry(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=250)
    question_no = models.IntegerField()
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class QuestionChoice(models.Model):
    title = models.CharField(max_length=250)
    point = models.IntegerField()

    def __str__(self):
        return self.title



class VoteCast(models.Model):
    voter = models.ForeignKey(NidInfo, on_delete=models.CASCADE)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ministry.name