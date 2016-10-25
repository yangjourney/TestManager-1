from django import forms
from django.forms import ModelForm, Textarea
from .models import *

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
	
class CaseForm(ModelForm):
	class Meta:
		model = Case
		fields = ['creation_date', 'title', 'case_text']
		widgets = {
			'case_text': Textarea(attrs={'cols': 80, 'rows':3})
		}		