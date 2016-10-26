from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.forms import inlineformset_factory
from .models import Case, Step
import sys
from .forms import *

class IndexView(generic.ListView):
    template_name = 'testlibrary/index.html'
    context_object_name = 'case_list'

    def get_queryset(self):
        return Case.objects.order_by('-creation_date')[:10]

class DetailView(generic.DetailView):
    model = Case
    template_name = 'testlibrary/detail.html'

def createcase(request):
    return render(request, 'testlibrary/createcase.html')

def submitnewcase(request):
    c = Case()
    try:
        c.title = request.POST['title']
        c.creation_date = timezone.now()
    except Exception as e:
        return render(request, 'testlibrary/createcase.html', {
            'error_message': "Something went wrong" + str(e),
            })
    c.save()
    return HttpResponseRedirect(reverse('testlibrary:index'))

def updatecase(request, pk):
	if request.method == 'POST':
		case_form = CaseForm(request.POST, instance=Case.objects.get(pk=pk))
		if case_form.is_valid():
			case_form.save()
		
			return HttpResponseRedirect(reverse('testlibrary:index'))
			
	return HttpResponse(str(request.POST.keys()) + str(request.POST.values()))
	

def case_form(request, case_id):
	case = Case.objects.get(pk=case_id)
	case_form_set = inlineformset_factory(Case, Step, fields=('step_text','result_text','order',), extra=0)
	args = {'case': case}
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		print(str(request.POST))
		test_file = open('test.log', 'a')
		with test_file:
			print(str(request.POST), file=test_file)
		# create a form instance and populate it with data from the request
		form = CaseForm(request.POST, instance=case, prefix='master')
		formset = case_form_set(request.POST, request.FILES, instance=case, prefix='steps')
			
		if form.is_valid() and formset.is_valid():
			try:
				form.save()		
				formset.save()					
				return HttpResponseRedirect(reverse('testlibrary:index'))
			except:
				print('exception when saving data')
		else:
			print('One of the forms did not pass validaiton')
			print(formset.errors)
			try:
				args['form'] = form				
				args['step_formset'] = formset
			except:
				print('exception when setting values')

			return render(request, 'testlibrary/casedetail.html', args)
	# if a GET method, create a blank form
	else:		
		form = CaseForm(instance=case, prefix='master')
		formset = case_form_set(instance=case, prefix='steps')
	return render(request, 'testlibrary/casedetail.html', {'form': form, 'step_formset':formset, 'case': case})
	
def deletecase(request, pk):
	case = Case.objects.get(pk=pk)
	case.delete()
	return HttpResponseRedirect(reverse('testlibrary:index'))
	