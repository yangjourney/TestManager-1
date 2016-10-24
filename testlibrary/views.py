from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from .models import Case, Step

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
# Create your views here.
