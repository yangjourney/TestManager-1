from django.db import models

class Case(models.Model):
    case_text = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date published')

class Step(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    step_text = models.CharField(max_length=200)
    result_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)


# Create your models here.
