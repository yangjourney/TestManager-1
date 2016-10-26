from django.conf.urls import url

from . import views

app_name = 'testlibrary'
urlpatterns = [
        url(r'^$',views.IndexView.as_view(), name='index'),
        url(r'^(?P<case_id>[0-9]+)/$', views.case_form, name='casedetail'),
        url(r'^CreateCase/$', views.createcase, name='createcase'),
        url(r'^submitnewcase/$',views.submitnewcase, name='submitnewcase'),
		url(r'^updatecase/(?P<pk>[0-9]+)/$',views.updatecase, name='updatecase'),
		url(r'^deletecase/(?P<pk>[0-9]+)/$', views.deletecase, name='deletecase'),
		url(r'^testrunner/$', views.runnerindex, name='runnerindex'),
    ]
