from secrets import choice
from django.db import models
from django.contrib.auth.models import User
from numpy import maximum

# Create your models here.
class Test(models.Model):
    subject = models.CharField(max_length=50)
    maximum_score = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return self.subject
        
    
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.CharField(max_length=100)
    is_correct = models.BooleanField()
    def __str__(self):
        return self.choice
        
class Scores(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.IntegerField()
    score = models.DecimalField(decimal_places=2, max_digits=5)
    

    