from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    'Опрос'
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    startDate = models.DateField()
    finishDate = models.DateField()

    def __str__(self):
        return self.name


class Question(models.Model):
    'Вопрос'
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    text_q = models.CharField(max_length=300)

    def __str__(self):
        return self.text_q


class Option(models.Model):
    'Вариант ответа'
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True)
    option_text = models.CharField(max_length=100)

    def __str__(self):
        return self.option_text


class Submission(models.Model):
    'Заполненный опрос'
    userId = models.IntegerField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, related_name='question', on_delete=models.CASCADE)
    option = models.ForeignKey(
        Option, related_name='text_q', on_delete=models.CASCADE, null=True, blank=True)
    option_text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.option_text
