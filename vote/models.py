from django.db import models
from django.contrib.auth.models import User


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


class VoteCast(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.ministry.name