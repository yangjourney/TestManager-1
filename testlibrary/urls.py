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
		url(r'^release/$', views.ReleaseList.as_view(), name='releaseindex'),
		url(r'^release/new/$', views.createrelease, name='createrelease'),
		url(r'^release/(?P<pk>[0-9]+)/$', views.ReleaseDetailView.as_view(), name='releasedetail'),
		url(r'^release/delete/(?P<pk>[0-9]+)/$', views.delete_release, name='delete-release'),		
    ]
