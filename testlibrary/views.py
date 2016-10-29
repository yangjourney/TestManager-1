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
    # The following statement could return an index error if the queryset is emtpy
	return CaseHistory.objects.filter(case=case).filter(revision_number=latest_revision)[0]

def case_form(request, case_id, revision_number = None):
    case = Case.objects.filter(pk=case_id).first()
    if case is None:
        return render(request, 'testlibrary/index.html', context={'messages': 'The specified test case does not exist'})
    case_form_set = inlineformset_factory(Case, Step, fields=('step_text','result_text','order'), extra=0)
    args = {'case': case}
    history_record = None
    latest_revision = CaseHistory.objects.filter(case=case).count()
    print('Latest revision is {!s}'.format(latest_revision))
    revision_number = request.GET.get('revision')
	# If a revision number was passed, find the associated history record
    if revision_number:
		# If the revision number is out of bounds, pick the latest revision
        if int(revision_number) > latest_revision or int(revision_number) < 1:
            history_record = GetLatestRevision(case)
        else:
            history_record = CaseHistory.objects.filter(case=case).filter(revision_number=revision_number)[0]
    else:		
        history_record = GetLatestRevision(case)
	
    print('Passed revision number {!s}'.format(revision_number))
    print('The history record is {!s}'.format(history_record.revision_number))
	# if this is a POST request we need to process the form data
    if request.method == 'POST':
		# create a form instance and populate it with data from the request
        form = CaseForm(request.POST, instance=case, prefix='master')
        form.fields['versions'].choices = [(x,x) for x in range(1, latest_revision+1)]
        formset = case_form_set(request.POST, request.FILES, instance=case, queryset=Step.objects.filter(case_version=history_record), prefix='steps')
		
        if form.is_valid() and formset.is_valid():
            try:
                revision = latest_revision + 1
                case.version += 1
				# NOTE: The CaseForm.save() method mutates the cleaned_data dictionary                
                form.save()
                history = CaseHistory(case=case, revision_number=revision)
                history.save()
                step_forms = formset.save(commit=False)
                print(step_forms)
                print('There are {!s} step forms'.format(len(step_forms)))
                print(request.POST)
                for step_form in step_forms:
                    new_step = Step(case=case, step_text=step_form.step_text,
                    result_text=step_form.result_text, order=step_form.order,
                    case_version=history)
                    print('saving new step')
                    new_step.save()
                return HttpResponseRedirect(reverse('testlibrary:casedetail', kwargs={'case_id': case.id}))
            except:
				# TODO: better error handling
                print('exception when saving data')
                raise
        else:
            print('One of the forms did not pass validaiton')   
            print(form.errors)
            print(formset.errors)
            try:
                args['form'] = form				
                args['step_formset'] = formset
            except:
                print('exception when setting values')

            return render(request, 'testlibrary/casedetail.html', args)
	# if a GET method, create the forms
    else:		
        form = CaseForm(instance=case, prefix='master', initial={'versions':history_record.revision_number, 'case_type':case.case_type})
        form.fields['versions'].choices = [(x,x) for x in range(1, latest_revision+1)]
        formset = case_form_set(instance=case, queryset=Step.objects.filter(case_version=history_record), prefix='steps')
        print('Get request formset: {!s}'.format(formset))
    return render(request, 'testlibrary/casedetail.html', {'form': form, 'step_formset':formset, 'case': case})
	
def deletecase(request, pk):
	case = Case.objects.get(pk=pk)
	case.delete()
	return HttpResponseRedirect(reverse('testlibrary:index'))
	
def delete_release(request, pk):
	Release.objects.get(pk=pk).delete()
	return HttpResponseRedirect(reverse('testlibrary:releaseindex'))