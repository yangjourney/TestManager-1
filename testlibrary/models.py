from django.db import models

class BusinessObject(models.Model):
	external_id = models.CharField(max_length=200, null=True)
    
	class Meta:
	    abstract = True

class CaseType(BusinessObject):
    case_type = models.CharField(max_length=200)
    def __str__(self):
        return self.case_type

class Case(BusinessObject):
    case_text = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default='TestCase')
    creation_date = models.DateTimeField('date published')
    version = models.IntegerField(default=1)
    case_type = models.ForeignKey('CaseType')

class CaseHistory(BusinessObject):
	revision_number = models.IntegerField(default=1)
	case = models.ForeignKey('Case', on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.revision_number)	


class Step(BusinessObject):		
    case = models.ForeignKey(Case)
    case_version = models.ForeignKey(CaseHistory, default=1)
    step_text = models.CharField(max_length=200)
    result_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)	
    class Meta:
        ordering = ['order']


class Release(BusinessObject):
	release_date = models.DateField()
	label = models.CharField(max_length=100)
	major_number = models.CharField(max_length=10)
	minor_number = models.CharField(max_length=10)
	
	#TODO: separate user-defined values for status into a different table
	STATUS_CHOICES = (
		('scheduled', 'Scheduled'),
		('in_progress', 'In Progress'),
		('complete', 'Complete'),
		('deployed', 'Deployed'),
	)
	
	status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='scheduled')
	
