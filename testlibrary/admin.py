from django.contrib import admin
from .models import Case, Step


#TODO: set up field sets

class StepInline(admin.TabularInline):
    model = Step

class CaseAdmin(admin.ModelAdmin):
    fields = ['creation_date', 'title', 'case_text']
    inlines = [StepInline]

    
admin.site.register(Case, CaseAdmin)
# Register your models here.
