from django.conf.urls import url

from . import views

app_name = 'testlibrary'
urlpatterns = [
        url(r'^$',views.IndexView.as_view(), name='index'),
        url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
        url(r'^CreateCase/$', views.createcase, name='createcase'),
        url(r'^submitnewcase/$',views.submitnewcase, name='submitnewcase'),
    ]
