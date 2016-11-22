from django import forms
from django.forms import ModelForm, Textarea
from .models import *

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
	
class CaseForm(ModelForm):
    versions = forms.ChoiceField()
    case_type = forms.ModelChoiceField(queryset=CaseType.objects.all())
    # Elements in this list will not be saved when the form is saved
    excluded_fields = ['versions'] 
	
    class Meta:
        model = Case
        fields = ['title', 'case_text', 'case_type']
        widgets = {'case_text': Textarea(attrs={'cols': 80, 'rows':3})}
	
    def save(self, *args, **kwargs):
        self.cleaned_data
        for field_name in self.excluded_fields:
            del self.cleaned_data[field_name]
        super(CaseForm, self).save(*args, **kwargs)
        
    
class DataFieldForm(ModelForm):
	class Meta:
		model = DataField
		fields = ['title', 'data_type']
    
class ReleaseForm(ModelForm):
	class Meta:
		model = Release
		fields = ['label', 'major_number', 'minor_number', 'status', 'release_date',]