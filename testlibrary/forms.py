from django import forms
from django.forms import ModelForm, Textarea
from .models import *

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
	
class CaseForm(ModelForm):

    class Meta:
        model = Case
        fields = ['creation_date', 'title', 'case_text']
        widgets = {'case_text': Textarea(attrs={'cols': 80, 'rows':3})}
        
    case_type = forms.ModelChoiceField(queryset=CaseType.objects.all())
    
    versions = forms.ModelChoiceField(
        queryset=CaseHistory.objects.all().order_by('revision_number'),
        empty_label = None
	)	
    
class ReleaseForm(ModelForm):
	class Meta:
		model = Release
		fields = ['label', 'major_number', 'minor_number', 'status', 'release_date',]