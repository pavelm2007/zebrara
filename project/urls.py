from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from common.views import *
from seo.views import get_file

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^grappelli/', include('grappelli.urls')),
                       url(r'^cked/', include('cked.urls')),
                       url(r'^feedback/', include('feedback.urls', namespace='feedback')),
                       url(r'^events/', include('events.urls', namespace='events')),
                       url(r'^works/', include('works.urls', namespace='works')),
                       url(r'^$', MainPage.as_view(), name='index'),
                       url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.MEDIA_ROOT}),
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                            'document_root': settings.STATIC_ROOT}),
)
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}),
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.STATIC_ROOT}),
    )