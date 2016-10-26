from django.db import models

class Case(models.Model):
    case_text = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default='TestCase')
    creation_date = models.DateTimeField('date published')
    version = models.IntegerField(default=1)

class Step(models.Model):		
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    step_text = models.CharField(max_length=200)
    result_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
	
    class Meta:
        ordering = ['order']


# Create your models here.
