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

class ReleaseList(generic.ListView):
		model = Release
	
class ReleaseDetailView(generic.DetailView):
	model = Release			
	
def createcase(request):
    return render(request, 'testlibrary/createcase.html')

def createrelease(request):
	if request.method == 'POST':
		form = ReleaseForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('testlibrary:releaseindex'))
		else:
			return render(request, 'testlibrary/createrelease.html', {'form': form})
	form = ReleaseForm()
	return render(request, 'testlibrary/createrelease.html', {'form': form})

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
    c_history = CaseHistory()
    c_history.case = c
    c_history.save()
    return HttpResponseRedirect(reverse('testlibrary:index'))

def updatecase(request, pk):
	if request.method == 'POST':
		case_form = CaseForm(request.POST, instance=Case.objects.get(pk=pk))
		if case_form.is_valid():
			case_form.save()
		
			return HttpResponseRedirect(reverse('testlibrary:index'))
			
	return HttpResponse(str(request.POST.keys()) + str(request.POST.values()))
	
def release_form(request, release_id):
	args = {}
	if request.method == 'POST':
		return HttpResponseRedirect(reverse('testlibrary:index'))
	else:
		return render(request, 'testlibrary/releasedetail.html', args)

		
def GetLatestRevision(case):
	latest_revision = CaseHistory.objects.filter(case=case).count()
	return CaseHistory.objects.filter(case=case).filter(revision_number=latest_revision)[0]

def case_form(request, case_id, revision_number = None):
	case = Case.objects.get(pk=case_id)
	case_form_set = inlineformset_factory(Case, Step, fields=('step_text','result_text','order'), extra=0)	
	args = {'case': case}
	default_history = None
	latest_revision = CaseHistory.objects.filter(case=case).count()
	if revision_number:
		if int(revision_number) > latest_revision:
			default_history = GetLatestRevision(case)
		else:
			default_history = CaseHistory.objects.filter(case=case).filter(revision_number=revision_number)[0]
	else:
		latest_revision = CaseHistory.objects.filter(case=case).count()
		default_history = CaseHistory.objects.filter(case=case).filter(revision_number=latest_revision)[0]
	print(str(default_history.case))
	print('case {0!s} has {1!s} revisions'.format(case_id, latest_revision))
	print('default history is {!s}'.format(str(default_history)))
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = CaseForm(request.POST, instance=case, prefix='master')
		formset = case_form_set(request.POST, request.FILES, instance=case, prefix='steps')
		
		if form.is_valid() and formset.is_valid():
			try:
				revision = latest_revision + 1
				case.version += 1			
				form.save()
				history = CaseHistory(case=case, revision_number=revision)
				history.save()
				step_forms = formset.save(commit=False)
				for step_form in step_forms:
					new_step = Step(case=case, step_text=step_form.step_text,
					result_text=step_form.result_text, order=step_form.order,
					case_version=history)
					new_step.save()				
				return HttpResponseRedirect(reverse('testlibrary:casedetail', kwargs={'case_id': case.id}))
			except:
				# TODO: better error handling
				print('exception when saving data')
				raise
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
		form.fields['versions'].queryset = CaseHistory.objects.filter(case=case)
		#formset = case_form_set(instance=case, prefix='steps')
		print('Test queryset: {!s}'.format(Step.objects.filter(case=case).filter(case_version=default_history)))
		formset = case_form_set(instance=case, queryset=Step.objects.filter(case_version=default_history), prefix='steps')
	return render(request, 'testlibrary/casedetail.html', {'form': form, 'step_formset':formset, 'case': case})
	
def deletecase(request, pk):
	case = Case.objects.get(pk=pk)
	case.delete()
	return HttpResponseRedirect(reverse('testlibrary:index'))
	
def delete_release(request, pk):
	Release.objects.get(pk=pk).delete()
	return HttpResponseRedirect(reverse('testlibrary:releaseindex'))
	