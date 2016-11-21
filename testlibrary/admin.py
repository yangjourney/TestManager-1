from django.contrib import admin
from .models import *


#TODO: set up field sets

class StepInline(admin.TabularInline):
    model = Step
    extra = 0

class StepAdmin(admin.ModelAdmin):
	fields = ['case', 'case_version', 'step_text', 'result_text', 'order']
	
class CaseAdmin(admin.ModelAdmin):
    fields = ['creation_date', 'title', 'case_text', 'case_type', 'data_sets']
    inlines = [StepInline]	

class CaseTypeAdmin(admin.ModelAdmin):
	fields = ['case_type']

class HistoryAdmin(admin.ModelAdmin):
	fields = ['revision_number', 'case']

class DataSetAdmin(admin.ModelAdmin):
	fields = ['title', 'data_fields']

class DataFieldAdmin(admin.ModelAdmin):
	fields = ['title', 'data_type']
	
admin.site.register(Case, CaseAdmin)
admin.site.register(CaseType, CaseTypeAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(CaseHistory, HistoryAdmin)
admin.site.register(DataSet, DataSetAdmin)
admin.site.register(DataField, DataFieldAdmin)

# Register your models here.
