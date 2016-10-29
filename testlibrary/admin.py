from django.contrib import admin
from .models import Case, Step, CaseType


#TODO: set up field sets

class StepInline(admin.TabularInline):
    model = Step

class CaseAdmin(admin.ModelAdmin):
    fields = ['creation_date', 'title', 'case_text']
    inlines = [StepInline]

class CaseTypeAdmin(admin.ModelAdmin):
	fields = ['case_type']
	
admin.site.register(Case, CaseAdmin)
admin.site.register(CaseType, CaseTypeAdmin)
# Register your models here.
