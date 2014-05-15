from django.conf.urls import *

from .views import *

urlpatterns = patterns('',
                       url(r'^service_example/(?P<pk>\d+)/$', ExampleServiceList.as_view(), name='example_service_list'),
                       url(r'^example/(?P<pk>\d+)/$', ExampleList.as_view(), name='example_category'),
                       url(r'^example_detail/(?P<pk>\d+)/$', ExampleDetail.as_view(), name='example_detail'),
                       url(r'^work/(?P<pk>\d+)/$', WorkDetail.as_view(), name='work_detail'),
                       url(r'^index/$', WorksIndex.as_view(), name='index'),
)